import os

host = os.environ.get("BIGIP_HOSTNAME")
user = os.environ.get("BIGIP_USERNAME")
pwd = os.environ.get("BIGIP_PASSWORD")

partition = os.environ.get("BIGIP_PARTITION")

datagroup_name = os.environ.get("BIGIP_PARTITION")