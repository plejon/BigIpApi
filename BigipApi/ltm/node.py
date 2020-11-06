import re
from typing import List, Dict

from requests import Response, session

from BigipApi.restclient import RestClient
from BigipApi.const import (
    default_partition,
    Node,
    url_node,
    build_uri,
)


class LtmNode:
    def __init__(self, *, hostname, username, password, token=None, verify_ssl=True):
        """
        Args:
            hostname (): fqdn or ip of bigip device
            username ():
            password ():
            token (): if supplied, username and password will be ignored.
            verify_ssl (): verifies valid SSL cert on bigip mgmt interface
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.token = token
        self.verify_ssl = verify_ssl

    @property
    def _client(self) -> session:
        client = RestClient(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            token=self.token,
            verify_ssl=self.verify_ssl,
        )

        return client

    def get_all_nodes(self, partition: str, select: List[str] = None) -> Response:
        """
        Get nodes from bigip device
        Args:
            select (): if set, will return only specified values from the bigip pool
                       example: ["name","partition","address"]
            partition (): if supplied, returns all nodes from that partition. else
            returns all nodes on the bigip device
        """
        uri = build_uri(uri=url_node, partition=partition, select=select)
        return self._client.get(uri)

    def get_node_by_ip(self, ip: str, partition: str = None) -> List[Dict]:
        """
        Get a node by the nodes ip adress
        Args:
            ip (): ip of node to get
            partition (): if not set, partition will be "Common"
        """
        node_list: List[Dict] = []
        for node in (
            self.get_all_nodes(partition=partition, select=["address", "name"])
            .json()
            .get("items")
        ):
            if ip == re.sub(r"%\d{0,3}$", "", node.get("address")):
                node_list.append(node)

        return node_list

    def check_if_node_exist(self, name: str, partition: str = default_partition) -> bool:
        """
        Check if a node exist on the bigip
        Args:
            name (): name of node
            partition (): if not set, partition will be "Common"

        Returns:
            True or False
        """
        uri = build_uri(uri=url_node, name=name, partition=partition)
        return self._client.get(uri=uri).ok

    def get_node(
        self, name: str, partition: str = default_partition, select: List[str] = None
    ) -> Response:
        """
        Return singel node
        Args:
            name (): name of node
            partition (): if not set, partition will be "Common"
        """
        uri = build_uri(uri=url_node, name=name, partition=partition)
        return self._client.get(uri=uri)

    def create_node(
        self, *, name: str, address: str, partition: str = default_partition
    ) -> Response:
        """
        Args:
            name (): name of node
            address (): ip adress
            partition (): if not set, partition will be "Common"
        """
        data = Node(name=name, address=address, partition=partition)
        return self._client.post(uri=url_node, body=data.__dict__)

    def delete_node(self, name: str, partition: str = default_partition) -> Response:
        """
        Args:
            name (): name of node
            partition (): if not set, partition will be "Common"
        """
        uri = build_uri(uri=url_node, name=name, partition=partition)
        return self._client.delete(uri=uri)
