from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_users.db import SQLAlchemyBaseUserTable

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[int]):
    username: Mapped[str] = mapped_column(String(24), unique=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.username!r}>"
