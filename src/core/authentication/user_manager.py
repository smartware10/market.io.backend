import logging
from typing import Optional, TYPE_CHECKING

from fastapi_users import BaseUserManager, IntegerIDMixin

from core.config import settings
from core.types.user_id import UserIdType
from core.models import User

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    # async def create(
    #     self,
    #     user_create: UserCreate,
    #     safe: bool = False,
    #     request: Optional["Request"] = None,
    # ) -> User:
    #
    #     await self.validate_password(user_create.password, user_create)
    #
    #     existing_user = await self.user_db.get_by_email(user_create.email)
    #     if existing_user is not None:
    #         raise exceptions.UserAlreadyExists()
    #
    #     user_dict = (
    #         user_create.create_update_dict()
    #         if safe
    #         else user_create.create_update_dict_superuser()
    #     )
    #     password = user_dict.pop("password")
    #     user_dict["hashed_password"] = self.password_helper.hash(password)
    #
    #     try:
    #         profile_data = user_dict.pop("profile")
    #     except KeyError:
    #         raise HTTPException(status_code=400, detail="Profile data is required.")
    #
    #     async with self.user_db.session as session:
    #         created_user = await self.user_db.create(user_dict)
    #
    #         if profile_data:
    #             profile = Profile(**profile_data, user_id=created_user.id)
    #             session.add(profile)
    #             await session.commit()
    #             await session.refresh(created_user)
    #
    #     await self.on_after_register(created_user, request)
    #
    #     return created_user

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )
