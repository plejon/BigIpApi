from typing import List, Dict

from requests import session, Response

from BigipApi.restclient import RestClient
from BigipApi.const import default_partition, CreateDataGroup, url_data_group


class LtmDataGroupEception(Exception):
    pass


class LtmDataGroup:
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
        self.name = None

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

    @staticmethod
    def _full_path(name: str, partition: str) -> str:
        return f"{url_data_group}/~{partition}~{name}"

    def get_data_group(self, name: str, partition=default_partition) -> Response:
        """
        Args:
            name (): name of data group
            partition (): if not set, partition will be "Common"
        """
        return self._client.get(uri=self._full_path(name, partition))

    def create_data_group(
        self,
        name: str,
        datagroup_type: str,
        /,
        partition: str = default_partition,
    ) -> Response:
        """
        Args:
            name (): Name of data group
            datagroup_type (): type: "ip", "integer" or "string"
            partition (): if not set, partition will be "Common"
        """
        body = CreateDataGroup(name=name, partition=partition, type=datagroup_type)

        return self._client.post(uri=url_data_group, body=body.__dict__)

    def delete_data_group(self, name: str, partition: str = default_partition) -> Response:
        """
        Args:
            name (): Name of data group
            partition (): if not set, partition will be "Common"
        """
        return self._client.delete(uri=self._full_path(name=name, partition=partition))

    def _get_existing_records(self, name, partition) -> List[Dict]:
        dg = self._client.get(uri=self._full_path(name=name, partition=partition))
        if dg.ok:
            return dg.json().get("records", [])

        raise LtmDataGroupEception(f"Could not retrive Data Group records\n{dg.text}")

    def add_records(
        self, name, data: List[Dict], /, partition=default_partition
    ) -> Response:
        """
        Add record(s) to data group. will overwrite existing ones.
        Args:
            name (): Name of Data Group
            data (): list of dicts with 2 keys. 'name' and 'data'
                     example: [{"name": "11.11.11.11/32","data": "Ticket123"}]
            partition (): if not set, partition will be "Common"
        """
        data = self._get_existing_records(name=name, partition=partition) + data
        body = {"records": data}
        return self._client.patch(uri=self._full_path(name, partition), body=body)

    def replace_records(
        self, name, data: List[Dict], /, partition=default_partition
    ) -> Response:
        """
        Does a http GET on the datagroup, take existing records and adds new ones to
        a local list. then does http patch to update the data group
        Args:
            name (): Name of Data Group
            data ():
            partition (): if not set, partition will be "Common"
        """
        data = {"records": data}
        return self._client.patch(uri=self._full_path(name, partition), body=data)

    def remove_all_entries(self, name, partition=default_partition) -> Response:
        """
        Removes all existing data group records
        Args:
            name (): Name of Data Group
            partition (): if not set, partition will be "Common"
        """
        data = {"records": []}
        return self._client.patch(uri=self._full_path(name, partition), body=data)
