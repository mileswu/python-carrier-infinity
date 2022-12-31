"""Contains the ZoneStatus class"""
from enum import Enum
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import util


class Activity(Enum):
    """Represents an activity"""

    HOME = "home"
    AWAY = "away"
    SLEEP = "sleep"
    WAKE = "wake"
    MANUAL = "manual"
    VACATION = "vacation"


class FanSpeed(Enum):
    """Represents the fan speed"""

    OFF = "off"
    LOW = "low"
    MED = "med"
    HIGH = "high"


class ZoneStatus(object):
    """Stores the status of a specific zone"""

    def __init__(self, xml: Element):
        self.xml = xml

    def __repr__(self) -> str:
        return ET.tostring(self.xml, encoding="unicode")

    @property
    def name(self) -> str:
        """The name of the zone"""
        return util.get_xml_element_text(self.xml, "name")

    @property
    def current_activity(self) -> Activity:
        """The currently set activity of the zone"""
        return Activity[util.get_xml_element_text(self.xml, "currentActivity")]

    @property
    def current_temperature(self) -> int:
        """The current temperature of the zone"""
        return int(util.get_xml_element_text(self.xml, "rt"))

    @property
    def current_relative_humidity(self) -> int:
        """The current relative humidity of the zone"""
        return int(util.get_xml_element_text(self.xml, "rh"))

    @property
    def fan_speed(self) -> FanSpeed:
        """The current fan speed of the zone"""
        return FanSpeed[util.get_xml_element_text(self.xml, "rh")]

    @property
    def target_heating_temperature(self) -> int:
        """The target heating temperature of the zone"""
        return int(util.get_xml_element_text(self.xml, "htsp"))

    @property
    def target_cooling_temperature(self) -> int:
        """The target cooling temperature of the zone"""
        return int(util.get_xml_element_text(self.xml, "clsp"))
