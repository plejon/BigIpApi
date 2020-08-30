from requests import session, Response
from BigipApi.log import log
import urllib3


# disable insecure https warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RestClient:
    """
    REST api docs:
    https://clouddocs.f5.com/api/icontrol-rest/

    To get going fast with basic calls:
    https://support.f5.com/csp/article/K13225405
    """

    def __init__(self, hostname, username, password):
        self._client = None
        self.base_url = f"https://{hostname}"
        self.credentials = {
            "username": username,
            "password": password,
            "loginProviderName": "tmos",
        }

    @property
    def client(self):
        if not self._client:
            client = session()
            client.verify = False
            response = client.post(
                f"{self.base_url}/mgmt/shared/authn/login", json=self.credentials
            )
            if not response.ok:
                log.error(f"Could not Login with username {self.credentials['username']}")
            client.headers.update(
                {"X-F5-Auth-Token": response.json().get("token", {}).get("token")}
            )
            self._client = client

        return self._client

    def get(self, uri: str) -> Response:
        return self.client.get(f"{self.base_url}{uri}")

    def post(self, *, uri: str, body: dict) -> Response:
        return self.client.post(f"{self.base_url}{uri}", json=body)

    def patch(self, *, uri: str, body: dict) -> Response:
        return self.client.patch(f"{self.base_url}{uri}", json=body)

    def put(self, *, uri: str, body: dict) -> Response:
        return self.client.put(f"{self.base_url}{uri}", json=body)

    def delete(self, uri: str) -> Response:
        return self.client.delete(f"{self.base_url}{uri}")
