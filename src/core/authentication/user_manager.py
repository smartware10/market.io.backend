from typing import Optional, TYPE_CHECKING, Union

from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    InvalidPasswordException,
)

from core.schemas.user import UserCreate as UserCreateSchema
from core.types.user_id import UserIdType
from core.models import User as UserModel

from core.config import settings
from core.logger import logger as log

if TYPE_CHECKING:
    from fastapi import Request


class UserManager(IntegerIDMixin, BaseUserManager[UserModel, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    reset_password_token_lifetime_seconds: int = settings.access_token.lifetime_seconds
    reset_password_token_audience: str = (
        settings.access_token.reset_password_token_audience
    )

    verification_token_secret = settings.access_token.verification_token_secret
    verification_token_lifetime_seconds: int = settings.access_token.lifetime_seconds
    verification_token_audience: str = settings.access_token.verification_token_audience

    async def validate_password(
        self, password: str, user: Union[UserCreateSchema, UserModel]
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                "Password must be at least 8 characters long"
            )

        if len(password) > 128:
            raise InvalidPasswordException("Password must not exceed 128 characters")

        if password.isnumeric():
            raise InvalidPasswordException("Password cannot consist of digits only")

    async def on_after_register(
        self,
        user: UserModel,
        request: Optional["Request"] = None,
    ):
        log.info(
            "User %r has registered.",
            user.id,
        )

    async def on_after_forgot_password(
        self,
        user: UserModel,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.info(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )

    async def on_after_request_verify(
        self,
        user: UserModel,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.info(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )
