from BigipApi import LtmPool
from tests.get_env_vars import *


def test_ltm_pool():
    dg = LtmPool(
        hostname=host,
        username=user,
        password=pwd,
        partition=partition
    )