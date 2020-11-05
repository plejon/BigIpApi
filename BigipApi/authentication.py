from time import time

import requests
from requests import Session
from datetime import datetime

from BigipApi import const
from BigipApi.const import Credentials, url_base
from BigipApi import log


class AuthSession:
    cache = {}  # holds Tokens and timeout in unix timestamp in microseconds

    def __init__(self, *, hostname, username, password, token, verify_ssl):
        self.base_url = url_base + hostname
        self.hostname = hostname
        self.username = username
        self.password = password
        self.token = token
        self.verify_ssl = verify_ssl
        print()
        if not self.hostname:
            raise ValueError("hostname not set")

        if self.verify_ssl is False:
            import urllib3  # noaq
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @property
    def _credentials(self) -> Credentials:
        return Credentials(username=self.username, password=self.password)

    @property
    def bigipsession(self) -> Session:
        """Will try to get token or use supplied token"""
        client = Session()

        if self.verify_ssl is False:
            client.verify = False

        if self.token:
            self._save_supplied_token(hostname=self.hostname, token=self.token)

        if self._verify_token_ttl() is False:
            self._get_token(client)

        client.headers.update({const.header_token: self.cache[self.hostname]["token"]})

        return client

    @classmethod
    def _save_supplied_token(cls, *, hostname, token: str):
        """Save user supplied token to class variable 'cache'"""
        cls._save_token(hostname=hostname, token=token, ttl=9000000000000000)

    @classmethod
    def _save_token(cls, *, hostname, token: str, ttl: int):
        """Saves token plus ttl to class variable 'cache'"""
        cls.cache[hostname] = {"token": token, "ttl": ttl}

    @classmethod
    def _update_saved_token_ttl(cls, *, hostname):
        """Updates current token ttl to 7 hours 40 minutes"""
        cls.cache[hostname]["ttl"] += (const.Token.timeout - 600) * 1000000

    def get_token(self):
        """get Bigip token and return it to the user"""
        self._get_token()
        return self.cache[self.hostname]

    def _get_token(self, client: Session):
        """calls bigip to get a user token"""
        log.debug("will call bigip REST and request authentication token")
        response = client.post(
            self.base_url + const.url_login, json=self._credentials.__dict__
        )

        if not response.ok:
            raise Exception(f"Clould not login to '{self.hostname}'\n{response.text}")

        log.debug("Succesfully got bigip authentication token")

        data = response.json().get("token")
        self._save_token(
            hostname=self.hostname, token=data["token"], ttl=data["expirationMicros"]
        )

        self._extend_token_ttl()

    def _extend_token_ttl(self):
        """update user token to extent timeout, default is 20 minutes"""
        response = self.bigipsession.patch(
            f"{self.base_url}{const.url_token}{self.cache[self.hostname]['token']}",
            json=const.payload_token_patch,
        )

        if response.ok:
            self._update_saved_token_ttl(hostname=self.hostname)
            log.debug("updated token ttl to 8 hours")

        else:
            raise Exception(f"Unable to update token ttl\n{response.text}")

    def _verify_token_ttl(self) -> bool:
        """if saved token exists, devide by 1 milion to get timestamp in seconds"""
        if self.hostname in self.cache:
            log.debug(
                "Token timeout is UTC "
                + datetime.utcfromtimestamp(
                    self.cache[self.hostname].get("ttl") / 1000000
                ).strftime("%Y-%m-%d %H:%M:%S")
            )
            if int(self.cache[self.hostname].get("ttl") / 1000000) - int(time()) > 600:
                return True
            log.debug("Bigip authentication token has, or will expire within 10min")
            return False
        else:
            log.debug("No Bigip authentication token found")
            return False
