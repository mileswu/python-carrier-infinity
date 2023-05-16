"""api.py tests"""
import pytest
from python_carrier_infinity import Auth
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
async def test_fetch_locations() -> None:
    """Test fetching locations"""
    await Auth.login(username, password, client_id)

    with pytest.raises(Exception):
        await Auth.login(username, "", client_id)
    with pytest.raises(Exception):
        await Auth.login("", "", client_id)
