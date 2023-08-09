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
