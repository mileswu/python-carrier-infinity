"""Contains the Config class"""
from enum import Enum
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import util
from .status import TemperatureUnits
from .zoneconfig import ZoneConfig


class Mode(Enum):
    """Represents the HVAC mode"""

    OFF = "off"
    COOL = "cool"
    HEAT = "heat"
    AUTO = "auto"
    FAN_ONLY = "fanonly"


class Config(object):
    """Represents the config of a system"""

    def __init__(self, xml: Element):
        self.xml = xml

    def __repr__(self) -> str:
        return ET.tostring(self.xml, encoding="unicode")

    @property
    def zones(self) -> list["ZoneConfig"]:
        """The config of all enabled zones"""
        zones = []
        for zone_xml in self.xml.iter("zone"):
            if util.get_xml_element_text(zone_xml, "enabled") == "off":
                continue
            zones.append(ZoneConfig(zone_xml))
        return zones

    @property
    def temperature_units(self) -> TemperatureUnits:
        """The temperature units used"""
        return TemperatureUnits[util.get_xml_element_text(self.xml, "cfgem")]

    @property
    def mode(self) -> Mode:
        """The HVAC mode"""
        return Mode[util.get_xml_element_text(self.xml, "mode")]
