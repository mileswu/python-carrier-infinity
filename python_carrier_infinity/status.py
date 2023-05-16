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

    def __init__(self, data: dict):
        self.data = data

    def __str__(self) -> str:
        return f"""System Status:
            Timestamp: {str(self.timestamp)}
            Mode: {self.mode}
            Outside temperature: {self.outside_temperature}{self.temperature_units.name}
            Current operation: {self.current_operation}
            Current airflow: {self.airflow}
            Humidifier active: {self.humidifier_active}
            Zone Statuses:
                {''.join([str(zone) for zone in self.zones])}
        """

    @property
    def zones(self) -> list["ZoneStatus"]:
        """The status of all enabled zones"""
        if "zones" not in self.data:
            raise Exception("No zones are found for current system")

        zones = []
        for zone in self.data["zones"]:
            if zone["enabled"] == "off":
                continue
            zones.append(ZoneStatus(zone))
        return zones

    @property
    def timestamp(self) -> datetime:
        """The timestamp of the status report"""
        return datetime.fromisoformat(self.data["utcTime"])

    @property
    def mode(self) -> str:
        return self.data["mode"]

    @property
    def outside_temperature(self) -> int:
        """The outside air temperature"""
        return int(self.data["oat"])

    @property
    def temperature_units(self) -> TemperatureUnits:
        """The temperature units used"""
        return TemperatureUnits(self.data["cfgem"])

    @property
    def current_operation(self) -> str:
        """The current in progress operation for idu - indoor unit?!"""
        return self.data["idu"]["opstat"]

    @property
    def humidifier_active(self) -> bool:
        """The status of the humidifer"""
        if self.data["humid"] == "on":
            return True
        else:
            return False

    @property
    def airflow(self) -> int:
        """The current airflow in cfm for idu - indoor unit?!"""
        return self.data["idu"]["cfm"]
