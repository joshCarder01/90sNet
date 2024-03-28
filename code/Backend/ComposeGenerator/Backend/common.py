import json
import os
import random

import typing

__all__ = (
    'BASE_PATH',
    'get_ip',
)


BASE_PATH = os.path.abspath(os.path.dirname(__file__))

class strings_subnet:
    fmt = 'subnet'
    current = 'current_subnet'
    count = 'subnet_count'
    max = 'subnet_max'
    prev = 'previous_ips'

__location_networks: typing.Dict[str, typing.Dict[str, typing.Any]] = json.load(open(os.path.join(BASE_PATH, 'network.json'), 'r'))


def __rand_octet():
    return random.randint(2, 255)

def __rand_Max():
    return random.randint(20,50)

def get_ip(location: str):
    current_subnet = __location_networks[location].get(strings_subnet.current, None)
    subnet_count = __location_networks[location].get(strings_subnet.count, 0)
    subnet_max = __location_networks[location].get(strings_subnet.max, None)
    previous_ips: typing.List[str] = __location_networks[location].get(strings_subnet.prev, [])

    # Write other defaults
    if  current_subnet is None:
        current_subnet = __rand_octet()
        __location_networks[location][strings_subnet.current] = current_subnet
    if subnet_max is None:
        subnet_max = __rand_Max()
        __location_networks[location][strings_subnet.max] = subnet_max
    
    while True:
        output = __location_networks[location][strings_subnet.fmt].format(current_subnet, __rand_octet)
        if output in previous_ips:
            continue
        subnet_count += 1
        previous_ips.append(output)
        __location_networks[location][strings_subnet.prev] = previous_ips
        if subnet_count > subnet_max:
            __location_networks[location][strings_subnet.count] = 0
            __location_networks[location][strings_subnet.max] = __rand_Max()
            __location_networks[location][strings_subnet.current] = __rand_octet()
        return output

def _gateway():
    output = __location_networks['Sawyer'][strings_subnet.fmt].format(0,1)
    return output
    



