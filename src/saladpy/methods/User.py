class UserMethods:
    async def get_balance(self):
        return await self._get('profile/balance') # type: ignore