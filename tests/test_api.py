"""api.py tests"""
import pytest
from python_carrier_infinity import login
from . import username, password

@pytest.mark.asyncio
async def test_login() -> None:
    """Test valid and invalid logins"""
    await login(username, password)

    with pytest.raises(Exception):
        await login(username, "")
    with pytest.raises(Exception):
        await login("", "")
