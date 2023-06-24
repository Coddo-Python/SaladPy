import json

from typing import Optional
from pathlib import Path

from aiohttp import ClientSession
from .exceptions import *
from .methods import Methods


class SaladClient(Methods):
    BASE_API_URL = "https://app-api.salad.com"
    V1_API_URL = "https://app-api.salad.com/api/v1/"
    V2_API_URL = "https://app-api.salad.io/api/v2/"
    AUTH_API_URL = "https://app-api.salad.com/auth/"
    _DEBUG_PROXY = "http://localhost:8000"

    def __init__(
        self,
        accessToken: Optional[str] = None,
        cachePath: Optional[Path] = None,
        *args,
        **kwargs,
    ):
        self.cookies = {"sAccessToken": accessToken} if accessToken else {}
        self.cachePath = cachePath
        self.cached = False
        self.http = ClientSession(cookies=self.cookies, *args, **kwargs)
        if self.cachePath is not None:
            if self.cachePath.exists():
                if self.cachePath.stat().st_size > 0:  # File is not empty
                    self.http.cookie_jar.load(self.cachePath)
                    self.cached = True
                            
    async def close(self):
        """
        Closes aiohttp `ClientSession` safely
        Using any methods after calling `close` will not work
        """
        await self.http.close()

    async def login(self, email: str):
        """Gets the necessary authentication tokens required for API requests

        Args:
            email (str): Salad E-Mail

        Raises:
            SaladPyException: An error during Email Verification

        Returns:
            Callable: A function representing the `_verify` method, takes in otp as argument
        """
        if not self.cached:
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({"email": email, "termsAccepted": True})
            async with self.http.post(
                f"{self.V2_API_URL}authentication-sessions",
                data=payload,
                headers=headers, proxy=self._DEBUG_PROXY
            ) as r:
                try:
                    assert r.status == 204
                    # Ensure that the `sInitToken` cookie is correctly applied to the session
                    # If not done correctly, OTP verification will not work
                    self.http.cookie_jar.update_cookies(r.cookies)
                except AssertionError:
                    text = await r.text()
                    raise SaladPyException(
                        f"Error {r.status} during email verification! {text}"
                    )
                else:
                    return self._verify

    async def _verify(self, otp: str):
        """Verify using OTP sent to Salad E-Mail

        Args:
            otp (str): The OTP given by the user

        Raises:
            SaladPyException: An error during OTP verification

        Returns:
            Optional[Bool]: True if no errors occured
        """
        if not self.cached:
            headers = {
                "Content-Type": "application/json",
            }
            payload = {"passcode": str(otp)}
            cookies = {cookie.key: cookie.value for cookie in list(self.http.cookie_jar) }
            async with self.http.post(
                f"{self.V2_API_URL}authentication-sessions/verification",
                json=payload,
                headers=headers,
                cookies=cookies,
            ) as r:
                try:
                    cookies = list(self.http.cookie_jar)
                    assert r.status == 204
                    self.http.cookie_jar.update_cookies(r.cookies)
                    if self.cachePath is not None:
                        self.cachePath.touch(exist_ok=True)
                        self.http.cookie_jar.save(self.cachePath)
                except AssertionError:
                    text = await r.json()
                    raise SaladPyException(
                        f"Error {r.status} during OTP verification! {text}"
                    )
                else:
                    return True

    async def _req(self, method: str, endpoint: str, params: Optional[dict] = None):
        cookies = {cookie.key: cookie.value for cookie in list(self.http.cookie_jar) }
        async with self.http.request(
            method, f"{self.V1_API_URL}{endpoint}", params=params, cookies=self.cookies, proxy=self._DEBUG_PROXY
        ) as r:
            text = await r.text()
            try:
                assert r.status == 200
            except AssertionError:
                if (
                    "try refresh token" in text
                ):  # DO NOT convert to JSON as it's not always guaranteed to be JSON
                    # Refresh token
                    print("Token expired, refreshing...")
                    await self.refresh_token()
            else:
                return await r.json()

    async def refresh_token(self):
        cookies = {cookie.key: cookie.value for cookie in list(self.http.cookie_jar) }
        async with self.http.post(f"{self.AUTH_API_URL}session/refresh", cookies=cookies, proxy=self._DEBUG_PROXY) as r:
            print(r.status)
            text = await r.text()
            print(text)
            self.http.cookie_jar.update_cookies(r.cookies)
            self.http.cookie_jar.save(self.cachePath)

    async def _get(self, endpoint: str, params: Optional[dict] = None):
        return await self._req("GET", endpoint, params)

    async def _post(self, endpoint: str, params: Optional[dict] = None):
        return await self._req("POST", endpoint, params)
