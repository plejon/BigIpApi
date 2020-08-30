# Bigip API
This package was made to talk to BigIP iControl REST API.  
Feel free to add stuff

### Requirements 
> python 3.7+

### Install
```bash
pip install -e .
```
### Uninstall
```bash
pip uninstall BigipApi
```

## Getting Started
> Bigip Rest Docs  
https://clouddocs.f5.com/api/icontrol-rest/APIRef_tm_analytics.html

Example GET 
```python
>>> import BigipApi
>>> help(BigipApi)
[...]
>>> from BigipApi import RestClient
>>>
>>> help(r)
Help on RestClient in module BigipApi.restclient object:

class RestClient(builtins.object)
 |  RestClient(*, hostname, username, password)
 |
 |  REST api docs:
 |  https://clouddocs.f5.com/api/icontrol-rest/
 |
 |  To get going fast with basic calls:
 |  https://support.f5.com/csp/article/K13225405
 |
 |  Methods defined here:
 |
 |  __init__(self, *, hostname, username, password)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |
 |  delete(self, uri: str) -> requests.models.Response
 |
 |  get(self, uri: str) -> requests.models.Response
 |
 |  patch(self, *, uri: str, body: dict) -> requests.models.Response
 |
 |  post(self, *, uri: str, body: dict) -> requests.models.Response
 |
 |  put(self, *, uri: str, body: dict) -> requests.models.Response
 |
 |  ----------------------------------------------------------------------
 |  Readonly properties defined here:
 |
 |  client
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables (if defined)
 |
 |  __weakref__
 |      list of weak references to the object (if defined)
>>>
>>>
>>> r = RestClient(
...     hostname="lb.example.com", username="root", password="passwd"
... )
>>> dir(r)
['_client', 'base_url', 'client', 'credentials', 'delete', 'get', 'patch', 'post', 'put']
>>>
>>> r.base_url
'https://lb.example.com'
>>>
>>> partition = "Common"
>>> pool_name = "mypool"
>>> uri = f"/mgmt/tm/ltm/pool/~{partition}~{pool_name}"
>>>
>>>
>>> response = r.get(uri)
>>>
>>> import json
>>> print(json.dumps(response.json(), indent=2))
{
  "kind": "tm:ltm:pool:poolstate",
  "name": "mypool",
  "partition": "Common",
  "fullPath": "/Common/mypool",
  "generation": 1,
  "selfLink": "https://localhost/mgmt/tm/ltm/pool/~Common~mypool?ver=14.1.2.3",
  "allowNat": "yes",
  "allowSnat": "yes",
  "description": "desc",
  "ignorePersistedWeight": "disabled",
  "ipTosToClient": "pass-through",
  "ipTosToServer": "pass-through",
  "linkQosToClient": "pass-through",
  "linkQosToServer": "pass-through",
  "loadBalancingMode": "round-robin",
  "minActiveMembers": 0,
  "minUpMembers": 0,
  "minUpMembersAction": "failover",
  "minUpMembersChecking": "disabled",
  "monitor": "/Common/pinger",
  "queueDepthLimit": 0,
  "queueOnConnectionLimit": "disabled",
  "queueTimeLimit": 0,
  "reselectTries": 0,
  "serviceDownAction": "none",
  "slowRampTime": 10,
  "membersReference": {
    "link": "https://localhost/mgmt/tm/ltm/pool/~Common~mypool/members?ver=14.1.2.3",
    "isSubcollection": true
  }
}
```
