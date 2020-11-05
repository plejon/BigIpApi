from typing import List, Union

from requests import Response

from BigipApi.authentication import AuthSession


class RestClient(AuthSession):
    """
    REST api docs:
    https://clouddocs.f5.com/api/icontrol-rest/

    To get going fast with basic calls:
    https://support.f5.com/csp/article/K13225405
    """

    def get(self, uri: str) -> Response:
        return self.bigipsession.get(f"{self.base_url}{uri}")

    def post(self, *, uri: str, body: dict) -> Response:
        return self.bigipsession.post(f"{self.base_url}{uri}", json=body)

    def patch(self, *, uri: str, body: Union[dict, List]) -> Response:
        return self.bigipsession.patch(f"{self.base_url}{uri}", json=body)

    def put(self, *, uri: str, body: Union[dict, List]) -> Response:
        return self.bigipsession.put(f"{self.base_url}{uri}", json=body)

    def delete(self, uri: str) -> Response:
        return self.bigipsession.delete(f"{self.base_url}{uri}")
