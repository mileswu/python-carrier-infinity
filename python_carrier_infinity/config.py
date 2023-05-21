"""Contains the Config class"""
from enum import Enum
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import util
from .types import Mode, TemperatureUnits
from .zoneconfig import ZoneConfig
import json


class Config(object):
    """Represents the config of a system"""

    def __init__(self, data: dict):
        self.data = data

    def __str__(self) -> str:
        return f"""===System Config Information===
        Temperature unit: {self.temperature_units}
        HVAC mode: {self.mode}
        Zone configs:
            {("************************").join([str(zone) for zone in self.zones])}"""

    @property
    def zones(self) -> list["ZoneConfig"]:
        """The config of all enabled zones"""
        zones = []
        for zone in self.data["zones"]:
            if zone["enabled"] == "off":
                continue
            zones.append(ZoneConfig(zone))
        return zones

    @property
    def temperature_units(self) -> TemperatureUnits:
        """The temperature units used"""
        return TemperatureUnits(self.data["cfgem"])

    @property
    def mode(self) -> Mode:
        """The HVAC mode"""
        return Mode(self.data["mode"])
