from enum import Enum


class ActivityName(Enum):
    """Represents an activity"""

    HOME = "home"
    AWAY = "away"
    SLEEP = "sleep"
    WAKE = "wake"
    MANUAL = "manual"


class FanSpeed(Enum):
    """Represents the fan speed"""

    OFF = "off"
    LOW = "low"
    MED = "med"
    HIGH = "high"


class Mode(Enum):
    """Represents the HVAC mode"""

    OFF = "off"
    COOL = "cool"
    HEAT = "heat"
    AUTO = "auto"
    FAN_ONLY = "fanonly"


class TemperatureUnits(Enum):
    """Represents the unit of temperature"""

    CELCIUS = "C"
    FARENHEIT = "F"
