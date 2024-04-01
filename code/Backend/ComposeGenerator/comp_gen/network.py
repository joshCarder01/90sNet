"""
Storing location mapping for IPs
"""
from typing import Dict

from .common import _gateway, BasicConfig


import yaml

with open(BasicConfig.get_resources('network.yaml'), 'r') as ifile:
    NETWORK: Dict[str, Dict[str, str]] = yaml.load(ifile, yaml.SafeLoader)

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
