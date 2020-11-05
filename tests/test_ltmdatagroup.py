from BigipApi import LtmDataGroup
from BigipApi import log
import logging
import os


def test_LtmDataGroup():
    log.setLevel(logging.DEBUG)
    dg = LtmDataGroup(
        hostname=os.environ.get("BIGIPAPI_HOSTNAME"),
        username=os.environ.get("BIGIPAPI_USERNAME"),
        password=os.environ.get("BIGIPAPI_PASSWORD"),
        # token="VWMXVA43TB66WF2C3LC2T4PYEL",
        verify_ssl=True
    )

    name = "plejon_lab"

    create = dg.create_data_group(name, "ip")
    assert create.ok

    get = dg.get_data_group(name)
    assert get.ok

    add = dg.add_records(name, [{"name": "14.14.14.14/32", "data": "Ticket123"}])
    assert add.ok

    remove_entries = dg.remove_all_entries(name)
    assert remove_entries.ok

    delete = dg.delete_data_group(name)
    assert delete.ok

