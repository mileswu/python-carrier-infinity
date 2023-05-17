"""Contains the System class"""
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import util
from . import api
from .api import Auth
from .config import Config
from .location import Location
from .status import Status
from .zonestatus import Activity
from .gql_schemas import get_user_query, get_system_config_query, get_system_status_query, update_zone_config_query
import json
import asyncio


class System(object):
    """Represents a Carrier Infinity system"""

    def __init__(self, data: dict, location: Location, auth: api.Auth):
        self.system_id = data["serial"]
        self.name = data["name"]
        self.auth = auth
        self.location = location
        self.last_fetched_config: Config = None
        self.last_fetched_status: Status = None

    # for testing
    def __str__(self) -> str:
        return f"""=======================================
        System Id: {self.system_id}
        Name: {self.name}
        Location: {str(self.location)}"""

    async def status(self) -> "Status":
        """Fetch current system status"""
        response = await api.gql_request(get_system_status_query(self.system_id), self.auth)
        # print(json.dumps(response))
        # raise Exception("stopppping")

        if "data" not in response:
            raise Exception("No top-level data field in gql get status response")
        
        if "infinityStatus" not in response["data"]:
            raise Exception("No infinityStatus field in get status response data")

        status = Status(response["data"]["infinityStatus"])
        self.last_fetched_status = status
        return status

    async def config(self) -> "Config":
        """Fetch the current config of the system"""
        response = await api.gql_request(get_system_config_query(self.system_id), self.auth)
        # print(json.dumps(response))
        # raise Exception("stopppping")

        if "data" not in response:
            raise Exception("No top-level data field in gql get config response")
        
        if "infinityConfig" not in response["data"]:
            raise Exception("No infinityConfig field in get config response data")

        config = Config(response["data"]["infinityConfig"])
        self.last_fetched_config = config
        return config
    
    async def update_zone_config(self, zone_id: str, hold: str, hold_activity: Activity, otmr: str) -> "Config":
        """Update the specified zone config"""
        response = await api.gql_request(update_zone_config_query(self.system_id, zone_id, hold, hold_activity, otmr), self.auth)

        print("Before...")
        print(self.last_fetched_config)

        """Refresh config information"""
        print("Sleeping before refetching config...")
        await asyncio.sleep(5)
        await self.config()
        print("After...")
        print(self.last_fetched_config)



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
