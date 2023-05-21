"""Accessing and changing the config"""
from __future__ import annotations
from .types import ActivityName, FanSpeed, Mode, TemperatureUnits


class System:
    """Represents the top-level system config"""

    def __init__(self, data: dict):
        self.data = data

    def __str__(self) -> str:
        return f"""\
            Temperature unit: {self.temperature_units}
            HVAC mode: {self.mode}
            Zones:
                {("************************").join([str(zone) for zone in self.zones])}"""

    @property
    def zones(self) -> list[Zone]:
        """The config of all enabled zones"""
        zones = []
        for zone in self.data["zones"]:
            if zone["enabled"] == "off":
                continue
            zones.append(Zone(zone))
        return zones

    @property
    def temperature_units(self) -> TemperatureUnits:
        """The temperature units used"""
        return TemperatureUnits(self.data["cfgem"])

    @property
    def mode(self) -> Mode:
        """The HVAC mode"""
        return Mode(self.data["mode"])


class Zone:
    """Represents the zone config"""

    def __init__(self, data: dict):
        self.data = data

    def __str__(self) -> str:
        activities = "\n" + ("\n=======================\n").join(
            [
                "\t\t" + str(activity) + ": " + str(self.activities[activity])
                for activity in self.activities
            ]
        )
        return f"""\
            {self.name} Zone Config:
                Hold activity: {self.hold_activity}
                Otmr: {self.otmr}
                Activities: {activities}
        """

    @property
    def name(self) -> str:
        """The name of the zone"""
        return self.data["name"]

    @property
    def hold_activity(self) -> ActivityName | None:
        """The currently held activity"""
        if self.data["hold"] == "on":
            return ActivityName(self.data["holdActivity"])
        else:
            return None

    @property
    def otmr(self):
        """The time by which the hold expires; None if hold is indefinite"""
        return self.data["otmr"]

    @property
    def activities(self) -> dict[ActivityName, Activity]:
        """The configs for each activity type"""
        activities = {}

        for activity in self.data["activities"]:
            activity_type = ActivityName(activity["type"])
            activities[activity_type] = Activity(activity)
        return activities


class Activity:
    """Represents the activity config"""

    def __init__(self, data: dict):
        self._data = data

    def __str__(self) -> str:
        return f"""\
            {self.activity}
                Fan speed: {self.fan_speed}
                Target heating temperature: {self.target_heating_temperature}
                Target cooling temperature: {self.target_cooling_temperature}"""

    @property
    def activity(self) -> ActivityName:
        """The associated activity"""
        return ActivityName(self._data["type"])

    @property
    def fan_speed(self) -> FanSpeed:
        """The fan speed"""
        return FanSpeed(self._data["fan"])

    @property
    def target_heating_temperature(self) -> int:
        """The target heating temperature"""
        return int(self._data["htsp"])

    @property
    def target_cooling_temperature(self) -> int:
        """The target cooling temperature"""
        return int(self._data["clsp"])
