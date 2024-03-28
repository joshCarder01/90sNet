import typing
from Backend.config import BasicConfig
from common import get_ip

class DockerContainer:
    """
    Description class for docker containers, should be able to store the 
    necessary information to set everything up.
    """
    name: str
    image: str
    location: str
    __ip: str

    def __init__(self, **args) -> None:
        self.load(args)

    def load(self, d: dict):
        self.image = d['image']
        self.name = d.get('name', self.image)
        self.location = d['location']
        self.networks = {
                BasicConfig.INTERNAL_NET:
                    {
                        "ipv4_address": get_ip(self.location)
                    } 
            }
        if d.get('proxy', False):
            self.networks[BasicConfig.PROXY_NET] = None
        self.__other_options = d.get("other_options", {})
    
    @property
    def ip(self):
        return self.ip
    
    @property
    def name(self):
        return '{}_{}_{}'.format(self.image, self.location, self.ip)

    def service(self):
        return '{}_{}_{}'.format(self.image, self.location, self.ip)
    
    def raw_dictionary(self):

        output = {
            self.service(): dict(
                image= self.image,
                container_name= self.name,
                networks= self.networks,
                **self.__other_options
            )
        }
        return output

class ContainerSet:
    _containers: typing.List[DockerContainer] = []
    __count: int
    __image: str
    __location: str
    __other_options: typing.Dict[str, typing.Any]
    __proxy: bool

    @property
    def containers(self):
        return self._containers

    def __init__(self, **args):
        self.__count = args['count']
        self.__image = args['image']
        self.__location = args['location']
        self.__other_options = args.get('other_options', None)
        self.__proxy = args.get('proxy', False)

        self.__setup_containers()
    
    def __setup_containers(self):
        for i in self.__count:
            self._containers.append(
                DockerContainer(
                    image=self.__image,
                    location = self.__location,
                    other_options = self.__other_options,
                    proxy = self.__proxy
                )
            )

