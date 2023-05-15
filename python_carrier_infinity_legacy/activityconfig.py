"""Stores the ActivityConfig class"""
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import util
from .zonestatus import Activity
from .zonestatus import FanSpeed


class ActivityConfig(object):
    """Represents the config of an activity"""

    def __init__(self, xml: Element):
        self.xml = xml

    def __repr__(self) -> str:
        return ET.tostring(self.xml, encoding="unicode")

    @property
    def activity(self) -> Activity:
        """The associated activity"""
        return Activity(util.get_xml_attribute(self.xml, "id"))

    @property
    def fan_speed(self) -> FanSpeed:
        """The fan speed"""
        return FanSpeed(util.get_xml_element_text(self.xml, "fan"))

    @property
    def target_heating_temperature(self) -> int:
        """The target heating temperature"""
        return int(util.get_xml_element_text(self.xml, "htsp"))

    @property
    def target_cooling_temperature(self) -> int:
        """The target cooling temperature"""
        return int(util.get_xml_element_text(self.xml, "clsp"))
