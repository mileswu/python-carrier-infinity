"""Contains the System class"""
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import util
from . import api
from .api import Auth
from .config import Config
from .location import Location
from .status import Status
from .gql_schemas import get_user_query, get_system_config_query, get_system_status_query
import json


class System(object):
    """Represents a Carrier Infinity system"""

    def __init__(self, data: dict, location: Location, auth: api.Auth):
        self.system_id = data["serial"]
        self.name = data["name"]
        self.auth = auth
        self.location = location

    # for testing
    def __str__(self) -> str:
        return f"""=======================================
        System Id: {self.system_id}
        Name: {self.name}
        Location: {str(self.location)}"""

    async def status(self) -> "Status":
        """Fetch current system status"""
        response = await api.request(
            f"/systems/{self.system_id}/status", None, self.auth
        )
        xml = ET.fromstring(response)
        return Status(xml)

    async def config(self) -> "Config":
        """Fetch the current config of the system"""
        response = await api.gql_request(get_system_config_query(self.system_id), self.auth)
        # print(json.dumps(response))
        # raise Exception("stopppping")

        if "data" not in response:
            raise Exception("No top-level data field in gql get config response")
        
        if "infinityConfig" not in response["data"]:
            raise Exception("No infinityConfig field in get config response data")

        return Config(response["data"]["infinityConfig"])

class User(object):
    """Represents a Carrier Infinity user"""

    def __init__(self, data):
        self.data = data
        self.all_systems = None

    async def user(auth: Auth) -> "User":
        """Fetch user information"""
        response = await api.gql_request(get_user_query(auth.username), auth)
        # print(response)

        if "data" not in response:
            raise Exception("GQL response does not contain top-level data field")
        
        if "user" not in response["data"]:
            raise Exception("GQL response data did not contain user field")

        return User(response["data"]["user"])

    def get_all_systems(self, auth) -> list[System]:
        if self.all_systems != None:
            return self.all_systems

        all_systems = []
        for location in self.data["locations"]:
            loc = Location(location)
            for system in location["systems"]:
                all_systems.append(System(system["profile"], loc, auth))
        
        self.all_systems = all_systems
        return self.all_systems

async def systems(auth: Auth) -> list[System]:
    """Fetch list of all systems corresponding to user"""
    user = await User.user(auth)

    # all_systems = user.get_all_systems(auth)
    # for system in all_systems:
    #     print(system)
    
    # raise Exception("test")

    return user.get_all_systems(auth)
