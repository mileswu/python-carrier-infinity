"""Authentication and making GraphQL queries"""
from __future__ import annotations
import base64
from datetime import datetime, timedelta
import hashlib
import secrets
import string
import aiohttp

AUTH_CLIENT_ID = "0oa1ce7hwjuZbfOMB4x7"
AUTH_REDIRECT_URI = "com.carrier.homeowner:/login"


def create_sso_http_session():
    base_url = "https://sso.carrier.com"
    headers = {"Accept": "application/json"}
    return aiohttp.ClientSession(base_url, headers=headers)


class Auth:
    """Represents authentication to the API service"""

    def __init__(self, username: str):
        self.username = username
        self._access_token = None
        self._refresh_token = None
        self._expiry_time = None

    async def _update_token(self, session, extra_data):
        current_time = datetime.now()

        async with session.request(
            "POST",
            "/oauth2/default/v1/token",
            data={"client_id": AUTH_CLIENT_ID, "redirect_uri": AUTH_REDIRECT_URI}
            | extra_data,
        ) as response:
            response_json = await response.json()

        if "access_token" not in response_json:
            raise Exception("Access token was not found / granted")

        self._access_token = response_json["access_token"]
        self._refresh_token = response_json["refresh_token"]
        self._expiry_time = current_time + timedelta(
            seconds=response_json["expires_in"]
        )

    def force_expiration_for_test(self):
        self._expiry_time = datetime.now()

    async def get_access_token(self) -> str:
        """Returns an OAuth 2.0 access token"""
        if datetime.now() >= self._expiry_time:
            extra_data = {
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
            }
            async with create_sso_http_session() as session:
                await self._update_token(session, extra_data)

        return self._access_token


def random_alphanumeric(length: int) -> str:
    """Generate random string"""
    return "".join(
        secrets.choice(string.ascii_letters + string.digits) for i in range(length)
    )


async def get_session_token(
    session: aiohttp.ClientSession, username: str, password: str
) -> str:
    """Use login credentials to obtain session token"""
    async with session.request(
        "POST",
        "/api/v1/authn",
        json={
            "password": password,
            "username": username,
        },
    ) as response:
        response_json = await response.json()

    if "sessionToken" not in response_json:
        raise Exception("sessionToken missing")

    return response_json["sessionToken"]


async def get_code_and_code_verifier(
    session: aiohttp.ClientSession,
    session_token: str,
) -> tuple[str, str]:
    """Get short-lived code from redirect location param via code challenge & session token"""
    code_verifier = random_alphanumeric(64)

    # Base64 URL-encoded SHA256 hash
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .replace("=", "")
    )

    nonce = random_alphanumeric(64)
    state = "None"

    async with session.request(
        "GET",
        "/oauth2/default/v1/authorize",
        params={
            "nonce": nonce,
            "sessionToken": session_token,
            "response_type": "code",
            "code_challenge_method": "S256",
            "scope": "openid profile offline_access",
            "code_challenge": code_challenge,
            "redirect_uri": AUTH_REDIRECT_URI,
            "client_id": AUTH_CLIENT_ID,
            "state": state,
        },
        allow_redirects=False,
    ) as response:
        code = (
            response.headers["location"]
            .replace(AUTH_REDIRECT_URI + "?", "")
            .split("&")[0]
            .split("=")[1]
        )
    return (code, code_verifier)


async def get_access_and_refresh_token(
    username: str,
    session: aiohttp.ClientSession,
    code: str,
    code_verifier: str,
) -> Auth:
    """Use short-lived code to get access and refresh token"""

    extra_data = {
        "grant_type": "authorization_code",
        "code": code,
        "code_verifier": code_verifier,
    }
    auth = Auth(username)
    await auth._update_token(session, extra_data)
    return auth


async def login(username: str, password: str) -> Auth:
    """Login to the API and return an Auth object"""

    # Reference: https://developer.okta.com/docs/guides/implement-grant-type/authcodepkce/main/#create-the-proof-key-for-code-exchange # pylint: disable=line-too-long

    async with create_sso_http_session() as session:
        session_token = await get_session_token(session, username, password)
        code, code_verifier = await get_code_and_code_verifier(session, session_token)
        return await get_access_and_refresh_token(
            username, session, code, code_verifier
        )


async def gql_request(query: dict, auth: Auth) -> dict:
    """Make a GraphQL request"""
    url = "https://dataservice.infinity.iot.carrier.com/graphql"
    access_token = await auth.get_access_token()
    headers = {"Authorization": "Bearer " + access_token}

    async with aiohttp.ClientSession() as session:
        async with session.request(
            "POST", url, headers=headers, json=query
        ) as response:
            return await response.json()
