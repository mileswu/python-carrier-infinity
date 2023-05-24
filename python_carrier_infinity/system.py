"""Contains the System class"""
from __future__ import annotations
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import api, config
from .api import Auth
from .status import Status
from .types import ActivityName
from .gql_schemas import (
    get_user_query,
    get_config_query,
    get_status_query,
    update_zone_config_query,
    update_activity_query,
)
import json
import asyncio


class System:
    """Represents a Carrier Infinity system"""

    def __init__(self, data: dict, location: str, auth: api.Auth):
        self.system_id = data["serial"]
        self.name = data["name"]
        self.auth = auth
        self.location = location
        self.last_fetched_config: config.System = None
        self.last_fetched_status: Status = None

    # for testing
    def __str__(self) -> str:
        return f"""=======================================
        System Id: {self.system_id}
        Name: {self.name}
        Location: {self.location}"""

    async def status(self) -> "Status":
        """Fetch current system status"""
        response = await api.gql_request(get_status_query(self.system_id), self.auth)
        # print(json.dumps(response))
        # raise Exception("stopppping")

        if "data" not in response:
            raise Exception("No top-level data field in gql get status response")

        if "infinityStatus" not in response["data"]:
            raise Exception("No infinityStatus field in get status response data")

        status = Status(response["data"]["infinityStatus"])
        self.last_fetched_status = status
        return status

    async def fetch_config(self) -> config.System:
        """Fetch the current config of the system"""
        response = await api.gql_request(get_config_query(self.system_id), self.auth)
        # print(json.dumps(response))
        # raise Exception("stopppping")

        if "data" not in response:
            raise Exception("No top-level data field in gql get config response")

        if "infinityConfig" not in response["data"]:
            raise Exception("No infinityConfig field in get config response data")

        cfg = config.System(response["data"]["infinityConfig"])
        self.last_fetched_config = cfg
        return cfg

    async def update_zone_config(
        self,
        zone_id: str,
        hold: str,
        hold_activity: ActivityName,
        hold_until: str | None,
    ) -> config.System:
        """Update the specified zone config"""
        response = await api.gql_request(
            update_zone_config_query(
                self.system_id, zone_id, hold_activity, hold_until
            ),
            self.auth,
        )

        print("Before...")
        print(self.last_fetched_config)

        """Refresh config information"""
        print("Sleeping before refetching config...")
        await asyncio.sleep(5)
        await self.fetch_config()
        print("After...")
        print(self.last_fetched_config)

    async def update_zone_activity(
        self, zone_id: str, activity: ActivityName, cool_temp: int, heat_temp: int
    ):

        r = await api.gql_request(
            update_activity_query(
                self.system_id, zone_id, activity, cool_temp, heat_temp
            ),
            self.auth,
        )
        print(r)


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
            for system in location["systems"]:
                all_systems.append(System(system["profile"], location["name"], auth))

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
