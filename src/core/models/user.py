from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from core.types.user_id import UserIdType
from .base import Base
from .mixins import IdIntPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .post import Post
    from .profile import Profile


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    username: Mapped[str] = mapped_column(String(24), unique=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.username!r}>"

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
