from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IdIntPkMixin, UserRelationMixin


class Profile(IdIntPkMixin, UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(24))
    last_name: Mapped[str | None] = mapped_column(String(24))
    bio: Mapped[str | None]
