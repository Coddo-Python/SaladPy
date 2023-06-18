import json

from typing import Optional
from pathlib import Path

from aiohttp import ClientSession
from .exceptions import *
from .methods import Methods

class SaladClient(Methods):
    API_URL = 'https://app-api.salad.io/api/v1/'
    AUTH_API_URL = 'https://app-api.salad.io/api/v2/'
    
    def __init__(self, accessToken: Optional[str] = None, cachePath: Optional[Path] = None, *args, **kwargs):
        self.cookies =  {"sAccessToken": accessToken} if accessToken else {}
        self.cachePath = cachePath
        self.http = ClientSession(cookies=self.cookies, *args, **kwargs)
    
    async def login(self, email: str):
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"email":email,"termsAccepted": True})
        async with self.http.post(f"https://app-api.salad.com/api/v2/authentication-sessions", data=payload, headers=headers) as r:
            try:
                assert r.status == 204
                # print("resp cookie")
                # print(r.headers)
                # print("------------------")
                # print(r.cookies)
                # print("------------------")
                # # self.http.cookie_jar.update_cookies()
                # print(self.http.cookie_jar.filter_cookies('app-api.salad.com'))
                # print("---------------------")
                # print(list(self.http.cookie_jar))
            except AssertionError:
                text = await r.text()
                raise SaladPyException(f"Error {r.status} during email verification! {text}")
            else: 
                return self._verify
    
    async def _verify(self, otp: str):
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"passcode": str(otp)})
        async with self.http.post(f"https://app-api.salad.com/api/v2/authentication-sessions/verification", data=payload, headers=headers) as r:
            try:
                assert r.status == 204
                cookies = list(self.http.cookie_jar)
                print(cookies)
                print("-------------------------")
                print("Sucessfully logged in!")
                if self.cachePath is not None:
                    self.cachePath.touch(exist_ok=True)
                    with self.cachePath.open(mode="w") as f:
                        tokens = {cookie.key: cookie.value for cookie in cookies }
                        json.dump(tokens, f)
            except AssertionError:
                text = await r.json()
                raise SaladPyException(f"Error {r.status} during OTP verification! {text}")
            else: 
                return True
            
        
    async def _req(self, method: str, endpoint: str, params: Optional[dict] = None):
        async with self.http.request(
            method, f"{self.API_URL}{endpoint}", params=params
        ) as r:
            json = await r.text()
            try:
                print(json)
                assert r.status == 200
            except AssertionError:
                print("bro it errored out")
                print(f"json here: {json}")
                print(f"status; {r.status}")
                # raise SaladPyException(
                #     json
                # )
            else:
                return json


    async def _get(self, endpoint: str, params: Optional[dict] = None):
        return await self._req("GET", endpoint, params)
    
    async def _post(self, endpoint: str, params: Optional[dict] = None):
        return await self._req("POST", endpoint, params)