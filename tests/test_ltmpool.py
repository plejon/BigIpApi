from BigipApi import LtmPool, LtmNode
from BigipApi import log
import logging
import os


def node_operation(operation, name):
    log.setLevel(logging.DEBUG)
    node = LtmNode(
        hostname=os.environ.get("BIGIPAPI_HOSTNAME"),
        username=os.environ.get("BIGIPAPI_USERNAME"),
        password=os.environ.get("BIGIPAPI_PASSWORD"),
        verify_ssl=True
    )
    if operation == "create":
        create = node.create_node(name, address=name)
        assert create.ok
    if operation == "delete":
        delete = node.delete_node(name)
        assert delete.ok


def test_ltmpool():
    log.setLevel(logging.DEBUG)
    pool = LtmPool(
        hostname=os.environ.get("BIGIPAPI_HOSTNAME"),
        username=os.environ.get("BIGIPAPI_USERNAME"),
        password=os.environ.get("BIGIPAPI_PASSWORD"),
        # token="3I7GCVI7SXJZD35VARZ4NPGNIB",
        verify_ssl=True
    )
    name = "plejon_lab"
    monitor = "NE_gpmonitor_ping"
    nodes = ["10.252.252.252", "10.252.252.253"]

    create = pool.create_pool(name, monitor=monitor)
    assert create.ok

    get = pool.get_pool(name)
    assert get.ok

    get_all = pool.get_pools()
    assert get_all.ok

    check = pool.check_if_pool_exist(name)
    assert check is True

    for x in nodes:
        node_operation("create", x)

    set_members = pool.set_pool_members(name, port=8080, nodes=nodes)
    assert set_members.ok

    delete = pool.delete_pool(name)
    assert delete.ok

    for x in nodes:
        node_operation("delete", x)
