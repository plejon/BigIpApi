from BigipApi import LtmNode
from BigipApi.logger import log
import logging
import os


def test_ltmnode():
    log.setLevel(logging.DEBUG)
    node = LtmNode(
        hostname=os.environ.get("BIGIPAPI_HOSTNAME"),
        username=os.environ.get("BIGIPAPI_USERNAME"),
        password=os.environ.get("BIGIPAPI_PASSWORD"),
        token="IZUCGKWB57A3JRCRFAFDAGLNXW",
        verify_ssl=False
    )
    name = "plejon_node"
    address = "15.15.15.15"

    create = node.create_node(name=name, address=address)
    assert create.ok

    get = node.get_node(name)
    assert get.ok

    check = node.check_if_node_exist(name)
    assert check is True

    get_by_ip = node.get_node_by_ip(address)
    assert get_by_ip

    get_all = node.get_all_nodes("Common")
    assert get_all.ok

    delete = node.delete_node(name)
    assert delete.ok
