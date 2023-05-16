"""Stores the ActivityConfig class"""
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import util
from .zonestatus import Activity
from .zonestatus import FanSpeed


class ActivityConfig(object):
    """Represents the config of an activity"""

    def __init__(self, data: dict):
        self.data = data

    def __str__(self) -> str:
        return f"""
                Type: {self.activity}
                Fan speed: {self.fan_speed}
                Target heating: {self.target_heating_temperature}
                Target cooling: {self.target_cooling_temperature}"""

    @property
    def activity(self) -> Activity:
        """The associated activity"""
        return Activity(self.data["type"])

    @property
    def fan_speed(self) -> FanSpeed:
        """The fan speed"""
        return FanSpeed(self.data["fan"])

    @property
    def target_heating_temperature(self) -> int:
        """The target heating temperature"""
        return int(self.data["htsp"])

    @property
    def target_cooling_temperature(self) -> int:
        """The target cooling temperature"""
        return int(self.data["clsp"])
