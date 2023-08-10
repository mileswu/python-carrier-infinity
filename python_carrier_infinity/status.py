"""Accessing the current status"""
from __future__ import annotations
from textwrap import dedent, indent
from datetime import datetime
import dateutil
import dateutil.parser
from .types import ActivityName, FanSpeed, Mode, TemperatureUnits


class System:
    """Represents the top-level system status"""

    def __init__(self, data: dict):
        self.data = data

    def __str__(self) -> str:
        zones = "\n\n".join([str(zone) for zone in self.zones.values()])
        return dedent(
            f"""\
                Timestamp: {str(self.timestamp)}
                Mode: {self.mode}
                Temperature units: {self.temperature_units}
                Outside temperature: {self.outside_temperature}
                Current operation: {self.current_operation}
                Current airflow: {self.airflow}
                Humidifier active: {self.humidifier_active}
                Zones:""") \
        + "\n" + indent(zones, "  ")
    
    @property
    def zones(self) -> dict[str, Zone]:
        """The status of all enabled zones"""
        zones = {}
        for zone_data in self.data["zones"]:
            if zone_data["enabled"] == "off":
                continue
            zone = Zone(zone_data)
            zones[zone.id] = zone
        return zones

    @property
    def timestamp(self) -> datetime:
        """The timestamp of the status report"""
        return dateutil.parser.isoparse(self.data["utcTime"])

    @property
    def mode(self) -> Mode:
        """The HVAC mode"""
        return Mode(self.data["mode"])

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
        """The current operation in progress"""
        return self.data["idu"]["opstat"]

    @property
    def humidifier_active(self) -> bool:
        """The status of the humidifer"""
        if self.data["humid"] == "on":
            return True
        return False

    @property
    def airflow(self) -> int:
        """The current airflow in cfm"""
        return self.data["idu"]["cfm"]


class Zone:
    """Represents the status of a zone"""

    def __init__(self, data: dict):
        self.data = data

    def __str__(self) -> str:
        return dedent(
            f"""\
                ID: {self.id}
                Activity: {self.activity}
                Temperature: {self.temperature}
                Humidity: {self.relative_humidity}
                Fan speed: {self.fan_speed}
                Target heating temperature: {self.target_heating_temperature}
                Target cooling temperature: {self.target_cooling_temperature}""")

    @property
    def id(self) -> str:  # pylint: disable=invalid-name
        """The id of the zone"""
        return self.data["id"]

    @property
    def activity(self) -> ActivityName:
        """The configured activity"""
        return ActivityName(self.data["currentActivity"])

    @property
    def temperature(self) -> int:
        """The temperature"""
        return int(self.data["rt"])

    @property
    def relative_humidity(self) -> int:
        """The relative humidity"""
        return int(self.data["rh"])

    @property
    def fan_speed(self) -> FanSpeed:
        """The configured fan speed"""
        return FanSpeed(self.data["fan"])

    @property
    def target_heating_temperature(self) -> int:
        """The configured target heating temperature"""
        return int(self.data["htsp"])

    @property
    def target_cooling_temperature(self) -> int:
        """The configured target cooling temperature"""
        return int(self.data["clsp"])
