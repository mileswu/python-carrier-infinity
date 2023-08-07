"""api.py tests"""
import pytest
from python_carrier_infinity import login, systems
from python_carrier_infinity.types import ActivityName
from . import username, password


@pytest.mark.asyncio
async def test_login() -> None:
    """Test valid and invalid logins"""
    await login(username, password)

    with pytest.raises(Exception):
        await login(username, "")
    with pytest.raises(Exception):
        await login("", "")


@pytest.mark.asyncio
async def test_user_systems() -> None:
    """Test getting user's systems information"""
    auth = await login(username, password)

    await systems(auth)


# @pytest.mark.asyncio
# async def test_get_config() -> None:
#     """Test getting system's config"""
#     auth = await Auth.login(username, password)

#     all_systems = await systems(auth)

#     system = all_systems[1]

#     config = await system.config()

#     print("System: " + system.name)
#     print(config)

#     # uncomment below to print out the config
#     # raise Exception("testing config")


@pytest.mark.asyncio
async def test_get_status() -> None:
    """Test getting system's status"""
    auth = await login(username, password)

    all_systems = await systems(auth)

    system = all_systems["Bedroom"]

    status = await system.status()

    print("System: " + system.name)
    print(status)

    # uncomment below to print out the status
    # raise Exception("testing status")


@pytest.mark.asyncio
async def test_update_config() -> None:
    """Test getting system's config"""
    auth = await login(username, password)

    all_systems = await systems(auth)

    system = all_systems["Bedroom"]

    print("System: " + system.name)
    config = await system.fetch_config()

    await system.update_zone_config("1", "on", ActivityName.MANUAL, None)
    await system.update_zone_activity("1", ActivityName.MANUAL, 70, 60)

    # uncomment below for printouts
    # raise Exception("testing config")
