"""Authentication and making GraphQL queries"""
import base64
import hashlib
import secrets
import string
import aiohttp


class Auth:
    """Represents authentication to the API service"""

    def __init__(self, username: str, access_token: str):
        self.username = username
        self._access_token = access_token

    def get_access_token(self) -> str:
        """Returns an OAuth 2.0 access token"""
        # TODO: Add foo regarding if token is past expiration time
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
    client_id: str,
    session_token: str,
    redirect_uri: str,
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
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "state": state,
        },
        allow_redirects=False,
    ) as response:
        code = (
            response.headers["location"]
            .replace(redirect_uri + "?", "")
            .split("&")[0]
            .split("=")[1]
        )
    return (code, code_verifier)


async def get_access_token(
    session: aiohttp.ClientSession,
    client_id: str,
    code: str,
    code_verifier: str,
    redirect_uri: str,
) -> str:
    """Use short-lived code to get access token for GraphQL operations"""

    async with session.request(
        "POST",
        "/oauth2/default/v1/token",
        data={
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code,
            "code_verifier": code_verifier,
            "client_id": client_id,
        },
    ) as response:
        response_json = await response.json()

    if "access_token" not in response_json:
        raise Exception("Access token was not found / granted")

    return response_json["access_token"]


async def login(username: str, password: str) -> Auth:
    """Login to the API and return an Auth object"""

    # Reference: https://developer.okta.com/docs/guides/implement-grant-type/authcodepkce/main/#create-the-proof-key-for-code-exchange # pylint: disable=line-too-long

    base_url = "https://sso.carrier.com"
    client_id = "0oa1ce7hwjuZbfOMB4x7"
    redirect_uri = "com.carrier.homeowner:/login"
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession(base_url, headers=headers) as session:
        session_token = await get_session_token(session, username, password)
        code, code_verifier = await get_code_and_code_verifier(
            session, client_id, session_token, redirect_uri
        )
        access_token = await get_access_token(
            session, client_id, code, code_verifier, redirect_uri
        )

    return Auth(username, access_token)


async def gql_request(query: dict, auth: Auth) -> dict:
    """Make a GraphQL request"""
    url = "https://dataservice.infinity.iot.carrier.com/graphql"
    headers = {
        "Authorization": "Bearer " + auth.get_access_token(),
    }

    async with aiohttp.ClientSession() as session:
        async with session.request(
            "POST", url, headers=headers, json=query
        ) as response:
            return await response.json()
