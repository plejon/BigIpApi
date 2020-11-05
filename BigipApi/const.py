from dataclasses import dataclass
from typing import List, Dict

url_base = "https://"

url_login = "/mgmt/shared/authn/login"
url_token = "/mgmt/shared/authz/tokens/"

url_node = "/mgmt/tm/ltm/node"
url_node_from_partition = url_node + "?$filter=partition+eq+{}"

url_data_group = "/mgmt/tm/ltm/data-group/internal"

url_pool = "/mgmt/tm/ltm/pool"
url_all_pool = "/mgmt/tm/ltm/pool?$membersReference&expandSubcollections=true"
url_all_pool_partiton = "/mgmt/tm/ltm/pool?$filter=partition+eq+{}$membersReference&expandSubcollections=true"
header_token = "X-F5-Auth-Token"
payload_token_patch = {"timeout": 28800}
default_partition = "Common"


@dataclass
class Token:
    timeout: int = 28800
    header: str = "X-F5-Auth-Token"


@dataclass
class Credentials:
    username: str
    password: str
    loginProviderName: str = "tmos"


@dataclass
class Node:
    name: str
    partition: str
    address: str


@dataclass
class Pool:
    name: str
    partition: str
    monitor: str


@dataclass
class CreateDataGroup:
    name: str
    partition: str
    type: str
    records = List[Dict]
