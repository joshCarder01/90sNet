import json
import typing
from .common import get_ip, BasicConfig

class DockerContainer:
    """
    Description class for docker containers, should be able to store the 
    necessary information to set everything up.
    """
    _name: str
    image: str
    location: str

    def __init__(self, **args) -> None:
        self.load(args)

    def load(self, d: dict):
        self.image = d['image']
        self._name = d.get('name', None)
        self.location = d['location']
        self.networks = {
                BasicConfig.INTERNAL_NET:
                    {
                        BasicConfig.IP_ADDR: get_ip(self.location)
                    } 
            }
        if d.get('proxy', False):
            self.networks[BasicConfig.PROXY_NET] = None
        self.__other_options = d.get("other_options", {})
    
    @property
    def ip(self):
        return self.networks[BasicConfig.INTERNAL_NET][BasicConfig.IP_ADDR]
    
    @property
    def name(self):
        if self._name is None:
            return '{}_{}_{}'.format(self.image, self.location, self.ip)
        return self._name

    def service(self):
        return '{}_{}_{}'.format(self.image, self.location, self.ip)
    
    def raw_dictionary(self):

        output = dict(
                image= self.image,
                container_name= self.name,
                networks= self.networks
            )

        if self.__other_options is not None:
            output = dict(**output, **self.__other_options)
        return output
    
    def toJSON(self):
        return self.raw_dictionary()        

    def __str__(self):
        return json.dumps(
            self.raw_dictionary(),
            indent=4,
            sort_keys=True,
        )
    
    def __repr__(self):
        return f"DockerContainer({self.image}, {self.location}, {self.ip})"

class ContainerSet:
    _containers: typing.List[DockerContainer]

    @property
    def containers(self):
        return self._containers

    def __init__(self):
        self._containers = []

    def __setup_containers(self, **args):
        __count = args['count']
        __image = args['image']
        __location = args['location']
        __other_options = args.get('other_options', None)
        __proxy = args.get('proxy', False)
        for i in range(__count):
            self._containers.append(
                DockerContainer(
                    image=__image,
                    location = __location,
                    other_options = __other_options,
                    proxy = __proxy
                )
            )
    
    def __getitem__(self, index):
        return self.containers[index]
    
    def __iter__(self):
        return iter(self.containers)

    def append(self, other = None, **args):
        if other is not None:
            self._containers.extend(other.containers)
        else:
            self.__setup_containers(**args)

    def raw_dictionary(self):
        output = {}
        for i in self._containers:
            output[i.service()] = i.raw_dictionary()
        
        return output
    
    def __repr__(self) -> str:
        return repr(self.containers)
    
    def __str__(self):
        return json.dumps(
            [i.toJSON() for i in self.containers],
            indent=4,
            sort_keys=True,
        )

