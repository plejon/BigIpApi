from requests import Response
from .restclient import RestClient
from .structs import Node, Pool
from typing import List
import re


class LtmPool(RestClient):
    """
    Create Pool / Edit pool members:
    Takes pool-name, partition and list of ip's to create a new pool with node members.
    Check if a node/pool exist, else create it. Or/else just update pool member.
    The supplied node list will be the new members. There is no append memebers.

    Delete pool:
    deletes pool, leaves node objects as is on the BigIP.
    """

    def __init__(self, hostname: str, username: str, password: str, partition: str):
        super(LtmPool, self).__init__(hostname, username, password)
        self._client = None
        self._existing_nodes = None
        self.partition = partition

    @property
    def existing_nodes(self) -> List[Node]:
        if not self._existing_nodes:
            r = self.client.get("/mgmt/tm/ltm/node?$select=name,partition,address")
            self._existing_nodes = [Node(**x) for x in r.json().get("items")]
        return self._existing_nodes

    def node_exist(self, ip) -> bool:
        return any(
            # Convert bigip addr syntax '10.10.10.%1' -> ipv4 address.
            ip == re.sub(r"%\d{0,3}$", "", n.address)
            and self.partition == n.partition
            for n in self.existing_nodes
        )

    def create_node(self, ip: str) -> Response:
        node = Node(name=ip, partition=self.partition, address=ip)
        return self.client.post(uri="/mgmt/tm/ltm/node", body=node.__dict__)

    def pool_exist(self, name: str) -> bool:
        return self.client.get(uri=f"/mgmt/tm/ltm/pool/~{self.partition}~{name}").ok

    def create_pool(self, name: str, monitor: str) -> Response:
        body = Pool(name=name, partition=self.partition, monitor=monitor)
        return self.client.post(uri="/mgmt/tm/ltm/pool/", body=body.__dict__)

    def add_pool_members(
        self, pool_name: str, node_port: int, nodes: List[str]
    ) -> Response:

        if not nodes:
            body = {"members": []}
        else:
            body = {"members": [f"{x}:  {node_port}" for x in nodes]}

        uri = "/mgmt/tm/ltm/pool/" + f"~{self.partition}~{pool_name}"
        return self.client.patch(uri=uri, body=body)

    def delete_pool(self, pool_name):
        return self.client.delete(
            "/mgmt/tm/ltm/pool/" + f"~{self.partition}~{pool_name}"
        )
