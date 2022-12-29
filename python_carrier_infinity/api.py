"""Authentication and retrieving the list of systems"""
from __future__ import annotations

import aiohttp
import defusedxml.ElementTree as ET
import oauthlib.oauth1
from . import util


class Auth(object):
    """Represents a username and OAuth authentication token"""

    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token

    @classmethod
    async def login(cls, username: str, password: str) -> Auth:
        """Login to the API and return an Auth object"""

        data = (
            "<credentials>"
            f"<username>{username}</username>"
            f"<password>{password}</password>"
            "</credentials>"
        )
        response = await _request(
            "/users/authenticated", username, data, auth_token=None
        )
        xml = ET.fromstring(response)
        access_token_xml = util.get_xml_element(xml, "accessToken")
        if access_token_xml.text is None:
            raise Exception("Access token is empty")

        return Auth(username, access_token_xml.text)


async def request(url: str, data: str | None, auth: Auth) -> str:
    """Make a request to the API."""
    return await _request(url, auth.username, data, auth.token)


API_URL_BASE = "https://www.app-api.ing.carrier.com"
CLIENT_KEY = "8j30j19aj103911h"
CLIENT_SECRET = "0f5ur7d89sjv8d45"


async def _request(
    url: str,
    username: str,
    data: str | None,
    auth_token: str | None,
) -> str:
    """Make a request to the API."""

    url = API_URL_BASE + url

    oauth = oauthlib.oauth1.Client(
        client_key=CLIENT_KEY,
        client_secret=CLIENT_SECRET,
        resource_owner_key=username,
        resource_owner_secret=auth_token,
        realm=url,
    )

    if data:
        method = "POST"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {"data": data}
    else:
        method = "GET"
        headers = None
        body = None

    url, headers, body = oauth.sign(url, method, body, headers)

    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, headers=headers, data=body) as response:
            response_text = await response.text()
            return response_text
