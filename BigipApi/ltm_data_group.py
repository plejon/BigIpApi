from requests import Response
from BigipApi.restclient import RestClient
from BigipApi.structs import CreateDataGroup
from typing import Dict, List


class LtmDataGroup(RestClient):
    def __init__(self, *, hostname, username, password, data_group_name, partition):
        super().__init__(hostname, username, password)
        self.uri_ltm_data_group = "/mgmt/tm/ltm/data-group/internal"
        self.data_group_name = data_group_name
        self.partition = partition

    @property
    def full_uri(self):
        """Returns exact URL to the Data Group"""
        return f"{self.uri_ltm_data_group}/~{self.partition}~{self.data_group_name}"

    @property
    def existing_records(self):
        dg = self.get(uri=self.full_uri)
        if dg.ok:
            return dg.json().get("records")

    def get_data_group(self) -> Response:
        return self.client.get(url=self.full_uri)

    def create_data_group(self, data_group_type: str) -> Response:
        """data_group_type, str: can be ip, integer, or string"""
        body = CreateDataGroup(
            name=self.data_group_name,
            partition=self.partition,
            type=data_group_type
        )

        return self.post(uri=self.uri_ltm_data_group, body=body.__dict__)

    def delete_data_group(self) -> Response:
        return self.delete(uri=self.full_uri)

    def add_entry_to_data_group(self, data: List[Dict]) -> Response:
        """data must be a list of dicts with 2 keys. 'name' and 'data'.
         example: {"name": "11.11.11.11/32","data": "Ticket123"}
        """
        if self.existing_records:
            data = self.existing_records + data
        body = {"records": data}
        return self.put(uri=self.full_uri, body=body)

    def remove_entry_from_data_group(self, name) -> Response:
        records = []
        if self.existing_records:
            for x in self.existing_records:
                if name not in x.get('name'):
                    records.append(x)

        body = {"records": records}
        return self.put(uri=self.full_uri, body=body)
