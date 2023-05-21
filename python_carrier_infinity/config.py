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
                {("************************").join([str(zone) for zone in self.zones.values()])}"""

    @property
    def zones(self) -> dict[str, Zone]:
        """The config of all enabled zones"""
        zones = {}
        for zone_data in self.data["zones"]:
            if zone_data["enabled"] == "off":
                continue
            zone = Zone(zone_data)
            zones[zone.name] = zone
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
            ["\t\t" + str(activity) for activity in self.activities.values()]
        )
        return f"""\
            {self.name} Zone Config:
                Hold activity: {self.hold_activity}
                Hold until: {self.hold_until}
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
    def hold_until(self) -> str | None:
        """The time by which the hold expires; None if hold is indefinite"""
        return self.data["otmr"]

    @property
    def activities(self) -> dict[ActivityName, Activity]:
        """The configs for each activity"""
        activities = {}

        for activity_data in self.data["activities"]:
            activity = Activity(activity_data)
            activities[activity.name] = activity
        return activities


class Activity:
    """Represents the activity config"""

    def __init__(self, data: dict):
        self.data = data

    def __str__(self) -> str:
        return f"""\
            {self.name}
                Fan speed: {self.fan_speed}
                Target heating temperature: {self.target_heating_temperature}
                Target cooling temperature: {self.target_cooling_temperature}"""

    @property
    def name(self) -> ActivityName:
        """The activity name"""
        return ActivityName(self.data["type"])

    @property
    def fan_speed(self) -> FanSpeed:
        """The fan speed"""
        return FanSpeed(self.data["fan"])

    @property
    def target_heating_temperature(self) -> int:
        """The target heating temperature"""
        return int(self.data["htsp"])

    @property
    def target_cooling_temperature(self) -> int:
        """The target cooling temperature"""
        return int(self.data["clsp"])
