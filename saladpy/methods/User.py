"""A class containing all the User API endpoints"""
from typing import List, Dict, Union

from .types import *


class UserMethods(BaseClient):
    """A class containing all the User API endpoints"""

    async def profile(self) -> ProfileResponse:
        """Gets a User's Profile

        Returns:
            ProfileResponse: Info about the User's profile
        """
        return ProfileResponse(**await self._get(self.V1_API_URL, "profile"))

    async def balance(self) -> BalanceResponse:
        """Gets a User's Balance

        Returns:
            BalanceResponse: The user's currentBalance and lifetimeBalance
        """
        return BalanceResponse(**await self._get(self.V1_API_URL, "profile/balance"))

    async def xp(self) -> int:
        """Gets a User's xp

        Returns:
            int: Lifetime Xp
        """
        return (await self._get(self.V1_API_URL, "profile/xp"))["lifetimeXp"]

    async def referral_code(self) -> str:
        """Gets a User's referral code

        Returns:
            str: User's referral code
        """
        return (await self._get(self.V1_API_URL, "profile/referral-code"))["code"]

    async def referrals(self) -> List[ReferralsResponse]:
        """Gets a list of users that have used a User's code

        Returns:
            List[ReferralsResponse]: List of users that have used your referral code
        """
        result = await self._get(self.V1_API_URL, "profile/referrals")
        response = []
        for resp in result:
            ref_def = ReferralDefinition(**resp["referralDefinition"])
            resp.pop("referralDefinition", None)
            response.append(ReferralsResponse(referralDefinition=ref_def, **resp))
        return response

    async def redemptions(self) -> List[RedemptionsResponse]:
        """Gets a User's Redemptions

        Returns:
            List[RedemptionsResponse]: A list of a user's redemptions, will be empty if there are none
        """
        result = await self._get(self.V1_API_URL, "reward-vault")
        response = []
        for resp in result:
            if "code" not in resp:
                resp["code"] = ""
            response.append(RedemptionsResponse(**resp))
        return response

    async def one_day_earning_history(self) -> Dict[str, float]:
        """Gets a User's 1 day earning history

        Returns:
            Dict[str, float]: 1 Day earning history, where the key is a time and the value is a float, empty if no earning history
        """
        return await self._get(self.V2_API_URL, "reports/1-day-earning-history")  # type: ignore

    async def seven_day_earning_history(self) -> Dict[str, float]:
        """Gets a User's 7 day earning history

        Returns:
            Dict[str, float]: 7 Day earning history, where the key is a time and the value is a float, empty if no earning history
        """
        return await self._get(self.V2_API_URL, "reports/7-day-earning-history")  # type: ignore

    async def thirty_day_earning_history(self) -> Dict[str, float]:
        """Gets a User's 30 day earning history

        Returns:
            Dict[str, float]: 30 Day earning history, where the key is a time and the value is a float, empty if no earning history
        """
        return await self._get(self.V2_API_URL, "reports/30-day-earning-history")  # type: ignore

    async def avatars(self) -> List[AvatarsResponse]:
        """Gets a User's unlocked avatars

        Returns:
            List[AvatarsResponse]: List of unlocked avatars
        """
        return [AvatarsResponse(**resp) for resp in await self._get(self.V2_API_URL, "avatars")]  # type: ignore

    async def selected_avatar(self) -> Union[SelectedAvatarResponse, None]:
        """Gets a User's currently selected avatar

        Returns:
            SelectedAvatarResponse: Currently selected avatar
            None: If using the default avatar
        """
        resp = await self._get(self.V2_API_URL, "avatars/selected")  # type: ignore
        if resp == 404:
            return None
        return SelectedAvatarResponse(**resp)

    async def bonuses(self) -> Union[list, None]:
        """Gets a User's unclaimed bonuses

        Returns:
        TODO: Test what a list of bonuses would look like
            List: List of unclaimed bonuses
            None: If there are no unclaimed bonuses
        """
        resp = await self._get(self.V2_API_URL, "bonuses")  # type: ignore
        if resp == []:
            return None
        return resp
