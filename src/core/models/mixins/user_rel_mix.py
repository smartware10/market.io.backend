from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

from core.types.user_id import UserIdType

if TYPE_CHECKING:
    from core.models.user import User


class UserRelationMixin:
    _user_id_unique: bool = False
    _user_id_nullable: bool = False
    _user_id_ondelete: str | None = None
    _user_back_populates: str | None = None
    _user_uselist: bool | None = None

    @declared_attr
    def user_id(cls) -> Mapped[UserIdType]:
        return mapped_column(Integer,
            ForeignKey(
                "users.id",
                ondelete=cls._user_id_ondelete,
            ),
            unique=cls._user_id_unique,
            nullable=cls._user_id_nullable,
        )

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship(
            "User",
            back_populates=cls._user_back_populates,
            uselist=cls._user_uselist,
        )
