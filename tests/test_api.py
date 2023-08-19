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


@pytest.mark.asyncio
async def test_token_refresh() -> None:
    auth = await login(username, password)
    access_token1 = await auth.get_access_token()
    expiration1 = auth._expiry_time
    auth.force_expiration_for_test()
    access_token2 = await auth.get_access_token()
    expiration2 = auth._expiry_time
    assert access_token1 != access_token2
    assert expiration1 != expiration2
