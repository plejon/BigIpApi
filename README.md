# Bigip API
This package was made to talk to BigIP iControl REST API.
The first session will request a auth token from the bigip and also extend the timeout for that token to 8hours. 
the token is stored until the python process dies. can save tokens from multiple bigip devices.

### Requirements 
> python 3.8+

### Install
```bash
pip install git+https://github.com/plejon/BigipApi.git@master
```
### Uninstall
```bash
pip uninstall BigipApi
```

## Getting Started
> Bigip Rest Docs  
https://clouddocs.f5.com/api/icontrol-rest/APIRef_tm_analytics.html

> Available classes
``` 
>>> import BigipApi
>>> BigipApi.__all__
('LtmNode', 'LtmPool', 'LtmDataGroup')
```
> Example 
```python
>>> from BigipApi import LtmNode
>>> node = LtmNode(hostname="11.11.11.11",username="admin",password="secret", verify_ssl=False)
>>> new = node.create_node("testnode", address="10.10.10.10")

>>> new
<Response [200]>
>>> node.check_if_node_exist("testnode")

True
>>>
>>> new.json()
{'kind': 'tm:ltm:node:nodestate', 'name': 'testnode', 'partition': 'Common', 'fullPath': '/Common/testnode', 'generation': 108101469, 'selfLink': 'https://localhost/mgmt/tm/ltm/node/~Common~testnode?ver=14.1.2.6', 'address': '10.10.10.10', 'connectionLimit': 0, 'dynamicRatio': 1, 'ephemeral': 'false', 'fqdn': {'addressFamily': 'ipv4', 'autopopulate': 'disabled', 'downInterval': 5, 'interval': '3600'}, 'logging': 'disabled', 'monitor': 'default', 'rateLimit': 'disabled', 'ratio': 1, 'session': 'monitor-enabled', 'state': 'checking'}
>>>
>>> existing = node.get_node("testnode")

>>> existing
<Response [200]>
>>>
>>> import json
>>> print(json.dumps(existing.json(), indent=2))
{
  "kind": "tm:ltm:node:nodestate",
  "name": "testnode",
  "partition": "Common",
  "fullPath": "/Common/testnode",
  "generation": 108102593,
  "selfLink": "https://localhost/mgmt/tm/ltm/node/~Common~testnode?ver=14.1.2.6",
  "address": "10.10.10.10",
  "connectionLimit": 0,
  "dynamicRatio": 1,
  "ephemeral": "false",
  "fqdn": {
    "addressFamily": "ipv4",
    "autopopulate": "disabled",
    "downInterval": 5,
    "interval": "3600"
  },
  "logging": "disabled",
  "monitor": "default",
  "rateLimit": "disabled",
  "ratio": 1,
  "session": "monitor-enabled",
  "state": "down"
}
>>>
```
> View docs
```
>>> from BigipApi import LtmNode
>>> help(LtmNode)

Help on class LtmNode in module BigipApi.ltm.node:

class LtmNode(builtins.object)
 |  LtmNode(*, hostname, username, password, token=None, verify_ssl=True)
 |
 |  Methods defined here:
 |
 |  __init__(self, *, hostname, username, password, token=None, verify_ssl=True)
 |      Args:
 |          hostname (): fqdn or ip of bigip device
 |          username ():
 |          password ():
 |          token (): if supplied, username and password will be ignored.
 |          verify_ssl (): verifies valid SSL cert on bigip mgmt interface
 |
 |  check_if_node_exist(self, name: str, partition: str = 'Common') -> bool
 |      Check if a node exist on the bigip
 |      Args:
 |          name (): name of node
 |          partition (): if not set, partition will be "Common"
 |
 |      Returns:
 |          True or False
 |
 |  create_node(self, name: str, address: str = '', partition: str = 'Common') -> requests.models.Response
 |      Args:
 |          name (): name of node
 |          address (): ip adress
 |          partition (): if not set, partition will be "Common"
 |
 |  delete_node(self, name: str, partition: str = 'Common') -> requests.models.Response
 |      Args:
 |          name (): name of node
 |          partition (): if not set, partition will be "Common"
 |
 |  get_all_nodes(self, partition) -> requests.models.Response
 |      Get nodes from bigip device
 |      Args:
 |          partition (): if supplied, returns all nodes from that partition. else
 |          returns all nodes on the bigip device
 |
 |  get_node(self, name: str, partition: str = 'Common') -> requests.models.Response
 |      Return singel node
 |      Args:
 |          name (): name of node
 |          partition (): if not set, partition will be "Common"
 |
 |  get_node_by_ip(self, ip: str, partition: str = None, /) -> List[Dict]
 |      Get a node by the nodes ip adress
 |      Args:
 |          ip (): ip of node to get
 |          partition (): if not set, partition will be "Common"
 |
 |  ----------------------------------------------------------------------
:
```
