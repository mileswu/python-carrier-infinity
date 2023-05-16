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

@pytest.mark.asyncio
async def test_get_config() -> None:
    """Test getting user's systems information"""
    auth = await Auth.login(username, password, client_id)

    await systems(auth)
