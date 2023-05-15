"""Contains the Status class"""
from datetime import datetime
from enum import Enum
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import util
from .zonestatus import ZoneStatus


class TemperatureUnits(Enum):
    """Represents the unit of temperature"""

    CELCIUS = "C"
    FARENHEIT = "F"


class Status(object):
    """Stores the status of a system"""

    def __init__(self, xml: Element):
        self.xml = xml

    def __repr__(self) -> str:
        return ET.tostring(self.xml, encoding="unicode")

    @property
    def zones(self) -> list["ZoneStatus"]:
        """The status of all enabled zones"""
        zones = []
        for zone_xml in self.xml.iter("zone"):
            if util.get_xml_element_text(zone_xml, "enabled") == "off":
                continue
            zones.append(ZoneStatus(zone_xml))
        return zones

    @property
    def timestamp(self) -> datetime:
        """The timestamp of the status report"""
        return datetime.fromisoformat(util.get_xml_element_text(self.xml, "timestamp"))

    @property
    def outside_temperature(self) -> int:
        """The outside air temperature"""
        return int(util.get_xml_element_text(self.xml, "oat"))

    @property
    def temperature_units(self) -> TemperatureUnits:
        """The temperature units used"""
        return TemperatureUnits(util.get_xml_element_text(self.xml, "cfgem"))

    @property
    def current_operation(self) -> str:
        """The current in progress operation"""
        return util.get_xml_element_text(self.xml, "opstat")

    @property
    def humidifier_active(self) -> bool:
        """The status of the humidifer"""
        if util.get_xml_element_text(self.xml, "humid") == "on":
            return True
        else:
            return False

    @property
    def airflow(self) -> int:
        """The current airflow in cfm"""
        return int(util.get_xml_element_text(self.xml, "cfm"))
