"""system.py tests"""
import pytest
import python_carrier_infinity
from . import username, password

@pytest.mark.asyncio
async def test_systems() -> None:
    """Test fetching systems"""
    auth = await python_carrier_infinity.login(username, password)
    systems = await python_carrier_infinity.systems(auth)
    for system in systems.values():
        print(str(system))

@pytest.mark.asyncio
async def test_fetch_status() -> None:
    """Test fetching system status"""
    auth = await python_carrier_infinity.login(username, password)
    systems = await python_carrier_infinity.systems(auth)
    status = await list(systems.values())[0].fetch_status()
    print(str(status))