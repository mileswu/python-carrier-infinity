"""Contains the ZoneConfig class"""
from __future__ import annotations
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import util
from .activityconfig import ActivityConfig
from .zonestatus import Activity


class ZoneConfig(object):
    """Represents the config of a zone"""

    def __init__(self, data: dict):
        self.data = data

    def __str__(self) -> str:
        activities = "\n" + ("\n=======================\n").join(["\t\t" + str(activity) + ": " + str(self.activities[activity]) for activity in self.activities])
        return f"""{self.name} Zone Config:
            Hold activity: {self.hold_activity}
            Otmr: {self.otmr}
            Activities: {activities}
        """

    @property
    def name(self) -> str:
        """The name of the zone"""
        return self.data["name"]

    @property
    def hold_activity(self) -> Activity | None:
        """The currently held activity"""
        if self.data["hold"] == "on":
            return Activity(self.data["holdActivity"])
        else:
            return None

    @property
    def otmr(self):
        """The time by which the hold expires; None if hold is indefinite"""
        return self.data["otmr"]

    @property
    def activities(self) -> dict[Activity, ActivityConfig]:
        """The configs for each activity type"""
        activities = {}

        for activity in self.data["activities"]:
            activity_type = Activity(activity["type"])
            activities[activity_type] = ActivityConfig(activity)
        return activities
