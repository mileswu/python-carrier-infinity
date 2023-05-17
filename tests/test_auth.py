"""api.py tests"""
import pytest
from python_carrier_infinity import Auth, systems
from . import username, password, client_id


@pytest.mark.asyncio
async def test_login() -> None:
    """Test valid and invalid logins"""
    await Auth.login(username, password, client_id)

    with pytest.raises(Exception):
        await Auth.login(username, "", client_id)
    with pytest.raises(Exception):
        await Auth.login("", "", client_id)

@pytest.mark.asyncio
async def test_user_systems() -> None:
    """Test getting user's systems information"""
    auth = await Auth.login(username, password, client_id)

    await systems(auth)

# @pytest.mark.asyncio
# async def test_get_config() -> None:
#     """Test getting system's config"""
#     auth = await Auth.login(username, password, client_id)

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
    auth = await Auth.login(username, password, client_id)

    all_systems = await systems(auth)

    system = all_systems[1]

    status = await system.status()

    print("System: " + system.name)
    print(status)

    # uncomment below to print out the status
    # raise Exception("testing status")

@pytest.mark.asyncio
async def test_update_config() -> None:
    """Test getting system's config"""
    auth = await Auth.login(username, password, client_id)

    all_systems = await systems(auth)

    system = all_systems[1]

    print("System: " + system.name)
    config = await system.config()

    await system.update_zone_config("1", "off", None, None)

    # uncomment below for printouts
    # raise Exception("testing config")