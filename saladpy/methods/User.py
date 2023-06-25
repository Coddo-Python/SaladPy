from types import SimpleNamespace

class UserMethods:
    async def profile(self) -> SimpleNamespace:
        """Gets a User's Profile

        Returns:
            SimpleNamespace<currentBalance: float, lifetimeBalance: float>: The user's lifetime and current balance
        """
        return await self._get(self.V1_API_URL, 'profile') # type: ignore
    
    async def balance(self) -> SimpleNamespace:
        """Gets a User's Balance

        Returns:
            SimpleNamespace<email: str, extentions: Object, id: str, lastSeenApplicationVersion: str, termsAcceptedAt: str, termsVersion: str, username: str, viewedReferralOnboarding: bool>: Info about the User's Profile
        """
        return await self._get(self.V1_API_URL, 'profile/balance') # type: ignore
    
    async def xp(self) -> int:
        """Gets a User's xp

        Returns:
            int: Lifetime Xp
        """
        return (await self._get(self.V1_API_URL, 'profile/xp')).lifetimeXp # type: ignore
    
    async def referral_code(self) -> SimpleNamespace:
        """Gets a User's Profile

        Returns:
            str: User's referral code
        """
        return (await self._get(self.V1_API_URL, 'profile/referral-code')).code # type: ignore
    
    async def referral_code(self) -> SimpleNamespace:
        """Gets a list of users that have used a User's code

        Returns:
        # TODO: Test this and get exact type
            list: List of users 
        """
        return await self._get(self.V1_API_URL, 'profile/referrals') # type: ignore
    
    async def redemptions(self) -> SimpleNamespace:
        """Gets a User's Redemptions

        Returns:
            list[Object<code: str, id: str, name: str, price: float, status: str, timestamp: str>]: User's referral code
        """
        return await self._get(self.V1_API_URL, 'reward-vault') # type: ignore
    
    async def one_day_earning_history(self) -> SimpleNamespace:
        """Gets a User's 1 day earning history

        Returns:
            dict[str: float]: 1 Day earning history, where the key is a time and the value is a float
        """
        return await self._get(self.V2_API_URL, 'reports/1-day-earning-history', as_json=True) # type: ignore
    
    async def seven_day_earning_history(self) -> SimpleNamespace:
        """Gets a User's 7 day earning history

        Returns:
            dict[str: float]: 7 Day earning history, where the key is a time and the value is a float
        """
        return await self._get(self.V2_API_URL, 'reports/7-day-earning-history', as_json=True) # type: ignore
    
    async def thirty_day_earning_history(self) -> SimpleNamespace:
        """Gets a User's 30 day earning history

        Returns:
            dict[str: float]: 30 Day earning history, where the key is a time and the value is a float
        """
        return await self._get(self.V2_API_URL, 'reports/30-day-earning-history', as_json=True) # type: ignore
    
    async def avatars(self) -> SimpleNamespace:
        """Gets a User's unlocked avatars

        Returns:
            list[Object<description: str, id: str, imageUrl: str, name: str>]: List of unlocked avatars
        """
        return await self._get(self.V2_API_URL, 'avatars') # type: ignore
    
    async def selected_avatar(self) -> SimpleNamespace:
        """Gets a User's currently selected avatar

        Returns:
            Object<description: str, id: str, imageUrl: str, name: str>: Currently selected avatar
            None: If using the default avatar
        """
        resp = await self._get(self.V2_API_URL, 'avatars/selected') # type: ignore
        if resp == 404:
            return None
        return resp
    
    async def bonuses(self) -> SimpleNamespace:
        """Gets a User's unclaimed bonuses

        Returns:
        TODO: Test what a list of bonuses would look like
            List: List of unclaimed bonuses
            None: If there are no unclaimed bonuses
        """
        resp = await self._get(self.V2_API_URL, 'bonuses') # type: ignore
        if resp == []:
            return None
        return resp