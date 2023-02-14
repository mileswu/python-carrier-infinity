"""Contains the ZoneConfig class"""
from __future__ import annotations
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import util
from .activityconfig import ActivityConfig
from .zonestatus import Activity


class ZoneConfig(object):
    """Represents the config of a zone"""

    def __init__(self, xml: Element):
        self.xml = xml

    def __repr__(self) -> str:
        return ET.tostring(self.xml, encoding="unicode")

    @property
    def name(self) -> str:
        """The name of the zone"""
        return util.get_xml_element_text(self.xml, "name")

    @property
    def hold_activity(self) -> Activity | None:
        """The currently held activity"""
        if util.get_xml_element_text(self.xml, "hold") == "on":
            return Activity(util.get_xml_element_text(self.xml, "holdActivity"))
        else:
            return None

    @property
    def activities(self) -> dict[Activity, ActivityConfig]:
        """The configs for each activity"""
        activities = {}
        for activity_xml in self.xml.iter("activity"):
            activity = Activity(util.get_xml_attribute(activity_xml, "id"))
            activities[activity] = ActivityConfig(activity_xml)
        return activities
