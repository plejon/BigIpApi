from typing import List

from requests import session, Response

from BigipApi.const import url_pool, default_partition, Pool, build_uri

from BigipApi.restclient import RestClient


class LtmPool:
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
    def client(self) -> session:
        client = RestClient(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            token=self.token,
            verify_ssl=self.verify_ssl,
        )

        return client

    def get_pools(
        self, partition: str = None, select: List[str] = None, expand_subcollections=False
    ) -> Response:
        """
        Get all pools from a partition
        Args:
            expand_subcollections (): if True, includes members reference of pool(s)
            select (): if set, will return only specified values from the bigip pool
                       example: ["name","partition","address"]
                       example from sub objects ["membersReference/items/address"]
                               this will only yield pool memeber addresses
            partition (): if not set. return all pools form all partitions
        """
        uri = build_uri(
            uri=url_pool,
            partition=partition,
            select=select,
            expand_subcollections=expand_subcollections,
        )

        return self.client.get(uri=uri)

    def create_pool(
        self, *, name: str, monitor: str = "", partition=default_partition
    ) -> Response:
        """
        Args:
            name (): name of pool
            monitor (): which monitor to use
            partition (): if not set, partition will be "Common"
        """
        body = Pool(name=name, partition=partition, monitor=monitor)
        return self.client.post(uri=url_pool, body=body.__dict__)

    def set_pool_members(
        self,
        name: str,
        port: int = None,
        nodes: List[str] = None,
        partition=default_partition,
    ) -> Response:
        """
        Will set or replace all pool memebers
        Args:
            name (): name of pool
            port (): destination port for nodes
            nodes (): list of node names
            partition (): if not set, partition will be "Common"

        Returns:

        """
        if not nodes:
            body = {"members": []}
        else:
            body = {"members": [{"name": f"{x}:{port}"} for x in nodes]}

        uri = build_uri(uri=url_pool, name=name, partition=partition)
        return self.client.patch(uri=uri, body=body)

    def delete_pool(self, name: str, partition=default_partition) -> Response:
        """

        Args:
            name (): name of pool
            partition (): if not set, partition will be "Common"
        """
        uri = build_uri(uri=url_pool, name=name, partition=partition)
        return self.client.delete(uri)

    def get_pool(
        self,
        *,
        name: str,
        partition=default_partition,
        select: List[str] = None,
        expand_subcollections=False,
    ) -> Response:
        """
        Args:
            select (): if set, will return only specified values from the bigip pool
                       example: ["name","partition","address"]
                       example from sub objects ["membersReference/items/address"]
                               this will only yield pool memeber addresses
            expand_subcollections (): if true, give all data from sub items. like memebers
            name (): name of pool
            partition (): if not set, partition will be "Common"
        """
        uri = build_uri(
            uri=url_pool,
            name=name,
            partition=partition,
            expand_subcollections=expand_subcollections,
            select=select,
        )
        # uri = build_uri(url_pool, partition, select, expand_members)
        return self.client.get(uri=uri)

    def check_if_pool_exist(self, name: str, partition=default_partition) -> bool:
        """
        check if a pool exist on partition
        Args:
            name (): name of pool
            partition (): if not set, partition will be "Common"

        Returns:
            True or False
        """
        uri = build_uri(uri=url_pool, name=name, partition=partition)
        return self.client.get(uri=uri).ok
