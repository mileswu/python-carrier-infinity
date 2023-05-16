"""Authentication and retrieving the list of systems"""
from __future__ import annotations

import aiohttp
import base64
import defusedxml.ElementTree as ET
import oauthlib.oauth1
from . import util
import json


class Auth(object):
    """Represents a username and OAuth 2.0 authentication token"""
    """Docs: https://openapi.ing.carrier.com/Content/pdf/oauth2-spec.pdf"""

    def __init__(self, username: str, token: str, session_token: str = "", access_token: str = ""):
        self.username = username
        self.token = token
        self.session_token = session_token
        self.access_token = access_token

    @classmethod
    async def login(cls, username: str, password: str, client_id: str) -> Auth:
        """Login to the API and return an Auth object"""

        """Step 1: Use login credentials to obtain session token"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        data = json.dumps({
            "password": password,
            "username": username,
        })
        response = await _request(
            "/api/v1/authn", username, data, auth_token=None, headers=headers, base_url="https://sso.carrier.com"
        )

        parsed_json = json.loads(response)
        print(parsed_json)

        if "sessionToken" not in parsed_json:
            raise Exception("sessionToken missing")

        session_token = parsed_json["sessionToken"]
        print(session_token)

        """Step 2: Get short-lived code from redirect location param via code challenge & session token"""
        # https://developer.okta.com/docs/guides/implement-grant-type/authcodepkce/main/#create-the-proof-key-for-code-exchange
        import base64
        import uuid
        import hashlib

        def uuid4_string():
            return base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').replace('=', '') 

        code_verifier = uuid4_string() + uuid4_string() + uuid4_string()
        m = hashlib.sha256()
        m.update(code_verifier.encode('utf-8'))
        before_encode_challenge = m.digest()
        code_challenge = base64.urlsafe_b64encode(before_encode_challenge).decode('utf-8').replace('=', '') # Base64URL-encoded SHA256) hash

        nonce = str(uuid.uuid4())
        state = str(uuid.uuid4())

        redirect_uri = 'com.carrier.homeowner:/login'
        params = {
            "nonce": nonce,
            "sessionToken": session_token,
            "response_type": 'code',
            "code_challenge_method": 'S256',
            "scope": 'openid profile offline_access',
            "code_challenge": code_challenge,
            "redirect_uri": 'com.carrier.homeowner:/login',
            "client_id": client_id,
            "state": state
        }

        print(params)

        data = None
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": 'application/json'}

        redirect_location = await _request(
            "/oauth2/default/v1/authorize", username, data, auth_token=None, headers=headers, base_url="https://sso.carrier.com", params=params
        )

        # extract code from query param of the redirect location
        code = redirect_location.replace(redirect_uri + '?', '').split('&')[0].split('=')[1]

        print(redirect_location)
        print(code)

        """Step 3: Use short-lived code to get access token for graphql operations"""

        data = {
            "grant_type": 'authorization_code',
            "redirect_uri": redirect_uri,
            "code": code,
            "code_verifier": code_verifier,
            "client_id": client_id,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": 'application/json'}
        params = None

        print(data)

        response = json.loads(await _request("/oauth2/default/v1/token", username, data, auth_token=None, headers=headers, base_url="https://sso.carrier.com"))
        print(response)

        if "access_token" not in response:
            raise Exception("Access token was not found / granted")

        access_token = response["access_token"]
        print(access_token)

        raise Exception("testing stuff yknow")

        return Auth(username, "placeholder", session_token, access_token)


async def request(url: str, data: str | None, auth: Auth, headers: dict | None = None) -> str:
    """Make a request to the API."""
    return await _request(url, auth.username, data, auth.token, headers)


"""OpenAPI Specs: https://openapi.ing.carrier.com/docs"""
API_URL_BASE = "https://www.myinfinitytouch.carrier.com"
CLIENT_KEY = "8j30j19aj103911h"
CLIENT_SECRET = "0f5ur7d89sjv8d45"


async def _request(
    url: str,
    username: str,
    data: str | None,
    auth_token: str | None,
    headers: dict | None = None,
    base_url: str = '',
    params: dict | None = None
) -> str:
    """Make a request to the API."""

    if base_url == '':
        base_url = API_URL_BASE
    url = base_url + url

    if headers == None:
        headers = {}

    if data:
        method = "POST"
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        body = data
        print("POST")
    else:
        method = "GET"
        body = None

    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, headers=headers, data=body, params=params, allow_redirects=False) as response:
            if response.status == 302:
                return response.headers["location"]
            response_text = await response.text()
            return response_text
