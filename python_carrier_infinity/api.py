"""Authentication and retrieving the list of systems"""
from __future__ import annotations
import base64
import hashlib
import json
import uuid
import aiohttp


class Auth(object):
    """Represents authentication to the API service"""

    def __init__(self, username: str, access_token: str):
        self.username = username
        self._access_token = access_token

    def get_access_token(self):
        """Returns an OAuth 2.0 access token"""
        # TODO: Add foo regarding if token is past expiration time
        return self._access_token


async def login(username: str, password: str, client_id: str) -> Auth:
    """Login to the API and return an Auth object"""

    # Reference: https://developer.okta.com/docs/guides/implement-grant-type/authcodepkce/main/#create-the-proof-key-for-code-exchange

    base_url = "https://sso.carrier.com"
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession(base_url, headers=headers) as session:
        # Step 1: Use login credentials to obtain session token
        async with session.request(
            "POST",
            "/api/v1/authn",
            json={
                "password": password,
                "username": username,
            },
        ) as response:
            response_text = await response.text()
        response_json = json.loads(response_text)

        if "sessionToken" not in response_json:
            raise Exception("sessionToken missing")

        session_token = response_json["sessionToken"]

        # Step 2: Get short-lived code from redirect location param via code challenge & session token

        code_verifier = (
            base64.urlsafe_b64encode(uuid.uuid4().bytes)
            .decode("utf-8")
            .replace("=", "")
        )
        code_verifier *= 3

        sha256_hash = hashlib.sha256()
        sha256_hash.update(code_verifier.encode("utf-8"))
        code_challenge = (
            base64.urlsafe_b64encode(sha256_hash.digest())
            .decode("utf-8")
            .replace("=", "")
        )  # Base64 URL-encoded SHA256 hash

        nonce = str(uuid.uuid4())
        state = str(uuid.uuid4())

        redirect_uri = "com.carrier.homeowner:/login"
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

        # Step 3: Use short-lived code to get access token for GraphQL operations"""

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
            response_text = await response.text()
        response_json = json.loads(response_text)

        if "access_token" not in response_json:
            raise Exception("Access token was not found / granted")

        access_token = response_json["access_token"]

    return Auth(username, access_token)


async def gql_request(query: dict, auth: Auth):
    """GraphQL request wrapper"""
    method = "POST"
    headers = {
        "Authorization": "Bearer " + auth.get_access_token(),
        "Content-Type": "application/json",
    }
    url = "https://dataservice.infinity.iot.carrier.com/graphql"
    data = json.dumps(query)

    # print("Making gql request...")
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, headers=headers, data=data) as response:
            if response.status == 302:
                return response.headers["location"]
            response_text = await response.text()
            # print(response_text)
            return json.loads(response_text)
