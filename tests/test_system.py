# SPDX-FileCopyrightText: 2022-present @mileswu <mileswu@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""system.py tests"""
import time
import pytest
from python_carrier_infinity import login, get_systems
from python_carrier_infinity.types import ActivityName, FanSpeed, Mode
from . import USERNAME, PASSWORD

SLEEP_DURATION_AFTER_CHANGE = 5.0


@pytest.mark.asyncio
async def test_fetch_systems() -> None:
    """Test fetching systems"""
    auth = await login(USERNAME, PASSWORD)
    systems = await get_systems(auth)
    for system in systems.values():
        print(str(system))


@pytest.mark.asyncio
async def test_fetch_status() -> None:
    """Test fetching status"""
    auth = await login(USERNAME, PASSWORD)
    systems = await get_systems(auth)
    status = await list(systems.values())[0].get_status()
    print(str(status))


@pytest.mark.asyncio
async def test_fetch_config() -> None:
    """Test fetching config"""
    auth = await login(USERNAME, PASSWORD)
    systems = await get_systems(auth)
    config = await list(systems.values())[0].get_config()
    print(str(config))


@pytest.mark.asyncio
async def test_set_zone_activity_hold() -> None:
    """Test setting the activity hold"""
    auth = await login(USERNAME, PASSWORD)
    systems = await get_systems(auth)
    system = list(systems.values())[0]
    config = await system.get_config()
    zone = list(config.zones.values())[0]

    hold_activity = zone.hold_activity
    hold_until = zone.hold_until

    async def test(new_hold_activity: ActivityName, new_hold_until: str | None) -> None:
        await system.set_zone_activity_hold(zone.id, new_hold_activity, new_hold_until)
        time.sleep(SLEEP_DURATION_AFTER_CHANGE)
        new_config = await system.get_config()
        assert new_config.zones[zone.id].hold_activity == new_hold_activity
        assert new_config.zones[zone.id].hold_until == new_hold_until

    await test(ActivityName.AWAY, None)
    await test(ActivityName.SLEEP, "22:30")

    await system.set_zone_activity_hold(zone.id, hold_activity, hold_until)
    time.sleep(SLEEP_DURATION_AFTER_CHANGE)


@pytest.mark.asyncio
async def test_set_zone_activity_temp() -> None:
    """Test setting the activity target temperature"""
    auth = await login(USERNAME, PASSWORD)
    systems = await get_systems(auth)
    system = list(systems.values())[0]
    config = await system.get_config()
    zone = list(config.zones.values())[0]
    activity = zone.activities[ActivityName.MANUAL]

    cool_temp = activity.target_cooling_temperature
    heat_temp = activity.target_heating_temperature

    new_cool_temp = 90
    new_heat_temp = 50
    await system.set_zone_activity_temp(
        zone.id, activity.name, new_cool_temp, new_heat_temp
    )

    time.sleep(SLEEP_DURATION_AFTER_CHANGE)
    new_config = await system.get_config()
    assert (
        new_config.zones[zone.id].activities[activity.name].target_cooling_temperature
        == new_cool_temp
    )
    assert (
        new_config.zones[zone.id].activities[activity.name].target_heating_temperature
        == new_heat_temp
    )

    await system.set_zone_activity_temp(zone.id, activity.name, cool_temp, heat_temp)
    time.sleep(SLEEP_DURATION_AFTER_CHANGE)


@pytest.mark.asyncio
async def test_set_zone_activity_fan() -> None:
    """Test setting the activity fan speed"""
    auth = await login(USERNAME, PASSWORD)
    systems = await get_systems(auth)
    system = list(systems.values())[0]
    config = await system.get_config()
    zone = list(config.zones.values())[0]
    activity = zone.activities[ActivityName.MANUAL]

    original_fan_speed = activity.fan_speed
    new_fan_speed = FanSpeed.HIGH

    await system.set_zone_activity_fan(zone.id, activity.name, new_fan_speed)
    time.sleep(SLEEP_DURATION_AFTER_CHANGE)
    new_config = await system.get_config()
    assert (
        new_config.zones[zone.id].activities[activity.name].fan_speed == new_fan_speed
    )

    await system.set_zone_activity_fan(zone.id, activity.name, original_fan_speed)
    time.sleep(SLEEP_DURATION_AFTER_CHANGE)


@pytest.mark.asyncio
async def test_set_mode() -> None:
    """Test setting the mode"""
    auth = await login(USERNAME, PASSWORD)
    systems = await get_systems(auth)
    system = list(systems.values())[0]
    config = await system.get_config()

    original_mode = config.mode
    new_mode = Mode.OFF

    await system.set_mode(new_mode)
    time.sleep(SLEEP_DURATION_AFTER_CHANGE)
    new_config = await system.get_config()
    assert new_config.mode == new_mode

    await system.set_mode(original_mode)
    time.sleep(SLEEP_DURATION_AFTER_CHANGE)
