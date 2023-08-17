"""system.py tests"""
import time
import pytest
from python_carrier_infinity import login, get_systems
from python_carrier_infinity.types import ActivityName
from . import username, password

SLEEP_DURATION_AFTER_CHANGE = 5.0

@pytest.mark.asyncio
async def test_fetch_systems() -> None:
    """Test fetching systems"""
    auth = await login(username, password)
    systems = await get_systems(auth)
    for system in systems.values():
        print(str(system))

@pytest.mark.asyncio
async def test_fetch_status() -> None:
    """Test fetching system status"""
    auth = await login(username, password)
    systems = await get_systems(auth)
    status = await list(systems.values())[0].get_status()
    print(str(status))

@pytest.mark.asyncio
async def test_fetch_config() -> None:
    """Test fetching system config"""
    auth = await login(username, password)
    systems = await get_systems(auth)
    config = await list(systems.values())[0].get_config()
    print(str(config))

@pytest.mark.asyncio
async def test_set_zone_activity_hold() -> None:
    auth = await login(username, password)
    systems = await get_systems(auth)
    system = list(systems.values())[0]
    config = await system.get_config()
    zone = list(config.zones.values())[0]

    hold_activity = zone.hold_activity
    hold_until = zone.hold_until

    async def test(new_hold_activity:ActivityName, new_hold_until:str|None) -> None:
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
    auth = await login(username, password)
    systems = await get_systems(auth)
    system = list(systems.values())[0]
    config = await system.get_config()
    zone = list(config.zones.values())[0]
    activity = zone.activities[ActivityName.MANUAL]

    cool_temp = activity.target_cooling_temperature
    heat_temp = activity.target_heating_temperature

    new_cool_temp = 90
    new_heat_temp = 50
    await system.set_zone_activity_temp(zone.id, activity.name, new_cool_temp, new_heat_temp)
    time.sleep(SLEEP_DURATION_AFTER_CHANGE)
    new_config = await system.get_config()
    assert new_config.zones[zone.id].activities[activity.name].target_cooling_temperature == new_cool_temp
    assert new_config.zones[zone.id].activities[activity.name].target_heating_temperature == new_heat_temp

    await system.set_zone_activity_temp(zone.id, activity.name, cool_temp, heat_temp)
    time.sleep(SLEEP_DURATION_AFTER_CHANGE)