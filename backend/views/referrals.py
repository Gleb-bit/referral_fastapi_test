from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User, UserCode
from auth.serializers import TokenSerializer, UserReadSerializer
from auth.views import auth
from config import get_session
from core.sqlalchemy.crud import Crud
from core.sqlalchemy.orm import Orm
from serializers.referrals import (
    ReferrerCodeGetSerializer,
    ReferralCodeCreateSerializer,
    ReferralCodeGetSerializer,
    ReferralsSerializer,
)

referral_router = APIRouter()
user_code_crud = Crud(UserCode)


@referral_router.post("/set_ref_code/", response_model=ReferralCodeGetSerializer)
async def set_ref_code(
    ref_code: ReferralCodeCreateSerializer,
    session: AsyncSession = Depends(get_session),
    credentials: TokenSerializer = Depends(auth.get_current_user),
):
    user = await Orm.scalar(User, session, User.email == credentials.email)
    data = {**ref_code.model_dump(), "user_id": user.id}

    return await Orm.create(UserCode, data, session)


@referral_router.post("/delete_ref_code/")
async def delete_ref_code(
    session: AsyncSession = Depends(get_session),
    credentials: TokenSerializer = Depends(auth.get_current_user),
):
    user = await Orm.scalar(User, session, User.email == credentials.email)
    code = user.code
    if not code:
        raise HTTPException(401, "Code does not exist")

    await session.delete(code)
    await session.commit()

    return Response(status_code=204)


@referral_router.get("/get_ref_code/", response_model=ReferrerCodeGetSerializer)
async def get_ref_code(
    ref_email: str,
    session: AsyncSession = Depends(get_session),
    credentials: TokenSerializer = Depends(auth.get_current_user),
):
    user = await Orm.scalar(User, session, User.email == ref_email)
    if not user:
        raise HTTPException(401, "User not found")

    return ReferrerCodeGetSerializer(code=user.code.code)


@referral_router.get(
    "/get_referrals/{referrer_id}/", response_model=ReferralsSerializer
)
async def get_referrals(
    referrer_id: int,
    session: AsyncSession = Depends(get_session),
    credentials: TokenSerializer = Depends(auth.get_current_user),
):
    referrer = await Orm.scalar(User, session, User.id == referrer_id)

    if not referrer:
        raise HTTPException(401, "Referrer not found")

    if not referrer.code:
        return ReferralsSerializer(referrals=[])

    referrals = await Orm.where(User, User.refer_code == referrer.code.code, session)

    return ReferralsSerializer(
        referrals=[UserReadSerializer.from_orm(user) for user in referrals.scalars().all()]
    )
