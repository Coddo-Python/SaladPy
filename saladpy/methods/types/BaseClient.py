"""A base version of SaladClient used for type hinting"""
from typing import Optional


class BaseClient:
    """A base version of SaladClient used for type hinting"""
    V1_API_URL = "https://app-api.salad.com/api/v1/"
    V2_API_URL = "https://app-api.salad.com/api/v2/"
    AUTH_API_URL = "https://app-api.salad.com/auth/"

    async def _get(self, api_url: str, endpoint: str, params: Optional[dict] = None):
        pass

    async def _post(self, api_url: str, endpoint: str, params: Optional[dict] = None):
        pass

    async def close(self):
        pass

    async def login(self, email: str):
        pass

    async def _verify(self, otp: str):
        pass

    async def refresh_token(self):
        pass

    @property
    def cookies(self):
        pass
