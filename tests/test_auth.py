"""api.py tests"""
import pytest
from python_carrier_infinity import Auth
from . import username, password


@pytest.mark.asyncio
async def test_login() -> None:
    """Test valid and invalid logins"""
    await Auth.login(username, password)

    with pytest.raises(Exception):
        await Auth.login(username, "")
    with pytest.raises(Exception):
        await Auth.login("", "")
