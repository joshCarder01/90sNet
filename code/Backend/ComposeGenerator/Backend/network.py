"""
Storing location mapping for IPs
"""
from common import _gateway
from config import BasicConfig


import yaml

NETWORK = yaml.load(open(BasicConfig.NETWORK_YAML_PATH))

# NETWORK_CREATION=dict(
#     networks=dict(
#         uc_net=dict(
#             driver="bridge",
#             name='uc_net',
#             ipam=dict(
#                 driver='default',
#                 config=dict(
#                     subnet='10.0.0.0/8',
#                     gateway=_gateway(),
#                 )
#             ),
#         )
#     )
# )
