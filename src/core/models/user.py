from datetime import date, datetime
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from core.types.user_id import UserIdType
from .base import Base
from .mixins import IdIntPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[UserIdType]):

    username: Mapped[str] = mapped_column(String(24), nullable=True)
    first_name: Mapped[str] = mapped_column(String(24), nullable=True)
    last_name: Mapped[str] = mapped_column(String(24), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(24), nullable=True)
    birth_date: Mapped[date] = mapped_column(TIMESTAMP, nullable=True, default=None)
    registered_on: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)

    # profile: Mapped["Profile"] = relationship(
    #     "Profile",
    #     back_populates="user",
    #     lazy="joined",
    #     uselist=False,
    #     cascade="all, delete",
    # )
