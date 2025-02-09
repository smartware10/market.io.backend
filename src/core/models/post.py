from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IdIntPkMixin, UserRelationMixin


class Post(IdIntPkMixin, UserRelationMixin, Base):
    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    text: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
