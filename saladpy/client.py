import json

from typing import Optional
from pathlib import Path
from aiohttp import ClientSession
from types import SimpleNamespace

from .exceptions import *
from .methods import Methods


class SaladClient(Methods):
    """The main client allowing you to use the rest of the library.
    
    NOTE: If using `token`, do not call login or verify
    """
    V1_API_URL = "https://app-api.salad.com/api/v1/"
    V2_API_URL = "https://app-api.salad.com/api/v2/"
    AUTH_API_URL = "https://app-api.salad.com/auth/"

    def __init__(
        self,
        cachePath: Optional[Path] = None,
        token: Optional[str] = None,
        *args,
        **kwargs,
    ):
        self.cachePath = cachePath
        self.cached = False
        self.token = token
        self.http = ClientSession(*args, **kwargs)
        if not token:
            if self.cachePath is not None:
                if self.cachePath.exists():
                    if self.cachePath.stat().st_size > 0:  # File is not empty
                        self.http.cookie_jar.load(self.cachePath)
                        self.cached = True
                    
    @property
    def cookies(self):
        return {cookie.key: cookie.value for cookie in list(self.http.cookie_jar) }
    
    async def clear_cookies(self):
        self.http.cookie_jar.clear()
                            
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
                headers=headers
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
            async with self.http.post(
                f"{self.V2_API_URL}authentication-sessions/verification",
                json=payload,
                headers=headers,
                cookies=self.cookies,
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

    async def _req(self, api_url : str, method: str, endpoint: str, params: Optional[dict] = None, token: Optional[str] = None, *args, **kwargs):
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        elif self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        async with self.http.request(
            method, f"{api_url}{endpoint}", params=params, headers=headers
        ) as r:
            text = await r.text()
            try:
                assert r.status == 200
            except AssertionError:
                if (
                    "try refresh token" in text
                ):  # DO NOT convert to JSON as it's not always guaranteed to be JSON
                    # Refresh token
                    await self.refresh_token(**kwargs)
                    return await self._req(api_url, method, endpoint, params, token, *args, **kwargs)
                else:
                    return r.status
            else:
                return text

    async def refresh_token(self, **kwargs):
        headers = {
            'rid': 'session'
        }
        async with self.http.post(f"{self.AUTH_API_URL}session/refresh", headers=headers, **kwargs) as r:
            text = await r.text()
            if r.status == 200:
                self.http.cookie_jar.update_cookies(r.cookies)
                if self.cachePath is not None:
                    self.http.cookie_jar.save(self.cachePath)

    async def _get(self, api_url: str, endpoint: str, params: Optional[dict] = None, **kwargs):
        resp = await self._req(api_url, "GET", endpoint, params, **kwargs)
        if resp == 404:
            return resp
        return json.loads(resp)

    async def _post(self, api_url: str, endpoint: str, params: Optional[dict] = None, **kwargs):
        resp = await self._req(api_url, "POST", endpoint, params, **kwargs)
        if resp == 404:
            return resp
        return json.loads(resp)
