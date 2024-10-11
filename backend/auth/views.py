from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.serializers import UserSerializer, UserReadSerializer, TokenSerializer
from config import get_session, SECRET_KEY
from core.fastapi.auth import AuthEmail
from core.sqlalchemy.orm import Orm

auth = AuthEmail(SECRET_KEY, TokenSerializer)

auth_router = APIRouter()


@auth_router.post("/register/", response_model=UserReadSerializer)
async def register(
    user: UserSerializer,
    session: AsyncSession = Depends(get_session),
):
    hashed_password = auth.get_password_hash(user.password)
    data = {
        "email": user.email,
        "hashed_password": hashed_password,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "refer_code": user.refer_code,
    }

    return await Orm.create(User, data, session)


@auth_router.post("/login/")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await Orm.scalar(User, session, User.email == form_data.username)

    if not user:
        raise auth.get_credentials_exc("Invalid email")

    if not auth.verify_password(form_data.password, user.hashed_password):
        raise auth.get_credentials_exc()

    access_token, refresh_token = auth.get_tokens({"sub": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token}
