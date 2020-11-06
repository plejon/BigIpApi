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
url_pool_filter = "$filter=partition+eq+{}$membersReference&expandSubcollections=true"
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
    monitor: str = ""


@dataclass
class CreateDataGroup:
    name: str
    partition: str
    type: str
    records = List[Dict]


def build_uri(
    *,
    uri: str = None,
    name: str = None,
    partition: str = None,
    select: List[str] = None,
    expand_subcollections: bool = False,
):
    if name:
        uri += f"/~{partition}~{name}"
    if partition or select or expand_subcollections:
        uri += "?"
        if partition and not name:
            if not isinstance(partition, str):
                raise ValueError(f"partition should be a string, {partition=}")
            uri += f"$filter=partition+eq+{partition.strip()}"
            if select or expand_subcollections:
                uri += "&"

        if select:
            if not all([isinstance(x, str) for x in select]):
                raise ValueError(f"select should be list of strings, {select=}")
            uri += "$select=" + ",".join(select)
            if expand_subcollections:
                uri += "&"

        if expand_subcollections:
            if not isinstance(expand_subcollections, bool):
                raise ValueError(
                    f"expand_members should be a boolean, {expand_subcollections=}"
                )
            uri += "expandSubcollections=true"

    print()

    return uri
