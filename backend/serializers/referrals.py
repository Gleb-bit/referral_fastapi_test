from typing import Optional, List, Union

from pydantic import BaseModel, EmailStr, Field

from auth.serializers import UserReadSerializer


class ReferrerSerializer(BaseModel):
    email: EmailStr


class ReferralCodeCreateSerializer(BaseModel):
    code: str
    expiration_in_days: int = Field(gt=0)


class ReferralCodeGetSerializer(BaseModel):
    code: str


class ReferrerCodeGetSerializer(BaseModel):
    code: Optional[str]


class ReferralsSerializer(BaseModel):
    referrals: List[UserReadSerializer]
