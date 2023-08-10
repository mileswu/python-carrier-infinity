"""system.py tests"""
import pytest
from python_carrier_infinity import login, get_systems
from . import username, password

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