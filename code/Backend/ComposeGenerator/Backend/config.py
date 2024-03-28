
from common import BASE_PATH

import os

class BasicConfig:

    NETWORK_YAML_PATH=os.path.join(BASE_PATH, 'network.yaml')
    PROXY_NET='proxy_net'
    INTERNAL_NET='uc_net'