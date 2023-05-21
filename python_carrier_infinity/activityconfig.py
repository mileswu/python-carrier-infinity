"""Stores the ActivityConfig class"""
from .types import Activity, FanSpeed


class ActivityConfig(object):
    """Represents the config of an activity"""

    def __init__(self, data: dict):
        self._data = data

    def __str__(self) -> str:
        return f"""\
            {self.activity}
                Fan speed: {self.fan_speed}
                Target heating temperature: {self.target_heating_temperature}
                Target cooling temperature: {self.target_cooling_temperature}"""

    @property
    def activity(self) -> Activity:
        """The associated activity"""
        return Activity(self._data["type"])

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
