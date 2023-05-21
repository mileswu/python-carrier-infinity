"""Contains the ZoneStatus class"""
from __future__ import annotations
from enum import Enum
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from .types import ActivityName, FanSpeed


class ZoneStatus(object):
    """Stores the status of a specific zone"""

    def __init__(self, data: dict):
        self.data = data

    def __str__(self) -> str:
        return f""" Current status for Zone Id {self.id}:
                        Activity: {self.current_activity}
                        Temperature: {self.current_temperature}
                        Humidity: {self.current_relative_humidity}
                        Fan speed: {self.fan_speed}
                        Target heating: {self.target_heating_temperature}
                        Target cooling: {self.target_cooling_temperature}
                    ========================================================
        """

    @property
    def id(self) -> str:
        """The id of the zone"""
        return self.data["id"]

    @property
    def current_activity(self) -> ActivityName:
        """The currently set activity of the zone"""
        return ActivityName(self.data["currentActivity"])

    @property
    def current_temperature(self) -> int:
        """The current temperature of the zone"""
        return int(self.data["rt"])

    @property
    def current_relative_humidity(self) -> int:
        """The current relative humidity of the zone"""
        return int(self.data["rh"])

    @property
    def fan_speed(self) -> FanSpeed:
        """The current fan speed of the zone"""
        return FanSpeed(self.data["fan"])

    @property
    def target_heating_temperature(self) -> int:
        """The target heating temperature of the zone"""
        return int(self.data["htsp"])

    @property
    def target_cooling_temperature(self) -> int:
        """The target cooling temperature of the zone"""
        return int(self.data["clsp"])
