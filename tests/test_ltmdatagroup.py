from BigipApi import LtmDataGroup
from tests.get_env_vars import *


def test_create_data_group():
    dg = LtmDataGroup(
        hostname=host,
        username=user,
        password=pwd,
        data_group_name=datagroup_name,
        partition=partition
    )

    c = dg.create_data_group(data_group_type="ip")
    assert c.ok
    u = dg.add_entry_to_data_group([{"name": "13.13.13.13", "data": "myip13"}])
    print()
    assert u.ok
    r = dg.remove_entry_from_data_group("13.13.13.13/32")
    assert r.ok
    d = dg.delete_data_group()
    assert d.ok

