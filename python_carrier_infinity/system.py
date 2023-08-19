# SPDX-FileCopyrightText: 2022-present @mileswu <mileswu@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""Contains the System class"""
from __future__ import annotations
from textwrap import dedent
from . import api, config, status
from .types import ActivityName
from .gql_schemas import (
    get_user_query,
    get_config_query,
    get_status_query,
    update_zone_config_query,
    update_activity_query,
)


class System:
    """Represents a Carrier Infinity system"""

    def __init__(self, data: dict, location: str, auth: api.Auth):
        self.data = data
        self.location = location
        self.auth = auth

    @property
    def name(self) -> str:
        """The name"""
        return self.data["name"]

    @property
    def serial(self) -> str:
        """The serial number"""
        return self.data["serial"]

    def __str__(self) -> str:
        return dedent(
            f"""\
                Name: {self.name}
                Serial Number: {self.serial}
                Location: {self.location}"""
        )

    async def get_status(self) -> status.System:
        """Fetch current system status"""
        response = await api.gql_request(get_status_query(self.serial), self.auth)
        return status.System(response["data"]["infinityStatus"])

    async def get_config(self) -> config.System:
        """Fetch current system config"""
        response = await api.gql_request(get_config_query(self.serial), self.auth)
        return config.System(response["data"]["infinityConfig"])

    async def set_zone_activity_hold(
        self,
        zone_id: str,
        hold_activity: ActivityName | None,
        hold_until: str | None,
    ) -> None:
        """Set the activity hold of a zone"""
        hold_activity_string = hold_activity.value if hold_activity else None
        await api.gql_request(
            update_zone_config_query(
                self.serial, zone_id, hold_activity_string, hold_until
            ),
            self.auth,
        )

    async def set_zone_activity_temp(
        self, zone_id: str, activity: ActivityName, cool_temp: int, heat_temp: int
    ) -> None:
        """Set the target temperatures of an activity for a given zone"""
        await api.gql_request(
            update_activity_query(
                self.serial, zone_id, activity.value, cool_temp, heat_temp
            ),
            self.auth,
        )


async def get_systems(auth: api.Auth) -> dict[str, System]:
    """Fetch list of systems"""
    response = await api.gql_request(get_user_query(auth.username), auth)
    systems_dict = {}
    for location in response["data"]["user"]["locations"]:
        for system_data in location["systems"]:
            system = System(system_data["profile"], location["name"], auth)
            systems_dict[system.name] = system
    return systems_dict
