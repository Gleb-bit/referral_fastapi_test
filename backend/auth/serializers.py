from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSerializer(BaseModel):
    email: EmailStr
    password: str

    first_name: str
    last_name: Optional[str] = None

    refer_code: Optional[str] = None


class UserReadSerializer(BaseModel):
    id: int
    email: EmailStr

    first_name: str
    last_name: Optional[str]

    refer_code: Optional[str]

    class Config:
        from_attributes = True


class TokenSerializer(BaseModel):
    email: EmailStr
