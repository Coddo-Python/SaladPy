from typing import NamedTuple

class ProfileResponse(NamedTuple):
    email: str
    extensions: dict
    id: str
    lastSeenApplicationVersion: str
    termsVersion: str
    termsAcceptedAt: str
    username: str
    viewedReferralOnboarding: bool

class BalanceResponse(NamedTuple):
    currentBalance: float
    lifetimeBalance: float
    
class ReferralDefinition(NamedTuple):
    balanceThreshold: float
    bonusRate: float
    referrerBonus: float
    
class ReferralsResponse(NamedTuple):
    code: str
    dateEntered: str
    earnedBalance: float
    refereeId: str
    referralDefinition: ReferralDefinition
    referrerId: str
    
class RedemptionsResponse(NamedTuple):
    code: str
    id: str
    name: str
    price: float
    status: str
    timestamp: str

class AvatarsResponse(NamedTuple):
    description: str
    id: str
    imageUrl: str
    name: str

class SelectedAvatarResponse(AvatarsResponse):
    pass