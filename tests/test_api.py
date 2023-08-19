# SPDX-FileCopyrightText: 2022-present @mileswu <mileswu@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""api.py tests"""
import pytest
from python_carrier_infinity import login
from . import USERNAME, PASSWORD


@pytest.mark.asyncio
async def test_login() -> None:
    """Test valid and invalid logins"""
    await login(USERNAME, PASSWORD)

    with pytest.raises(Exception):
        await login(USERNAME, "")
    with pytest.raises(Exception):
        await login("", "")


@pytest.mark.asyncio
async def test_token_refresh() -> None:
    """Test access token refreshing"""
    auth = await login(USERNAME, PASSWORD)
    access_token1 = await auth.get_access_token()
    expiration1 = auth.expiry_time
    auth.force_expiration_for_test()
    access_token2 = await auth.get_access_token()
    expiration2 = auth.expiry_time
    assert access_token1 != access_token2
    assert expiration1 != expiration2
