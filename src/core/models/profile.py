# from datetime import date, datetime
#
# from sqlalchemy import String, TIMESTAMP
# from sqlalchemy.orm import Mapped, mapped_column
#
# from .base import Base
# from .mixins import IdIntPkMixin, UserRelationMixin
#
#
# class Profile(Base, IdIntPkMixin, UserRelationMixin):
#     _user_id_unique = True
#     _user_id_ondelete = "CASCADE"
#     _user_back_populates = "profile"
#     _user_uselist = False
#
#     username: Mapped[str] = mapped_column(String(24), nullable=True)
#     first_name: Mapped[str] = mapped_column(String(24), nullable=True)
#     last_name: Mapped[str] = mapped_column(String(24), nullable=True)
#     middle_name: Mapped[str] = mapped_column(String(24), nullable=True)
#     birth_date: Mapped[date] = mapped_column(TIMESTAMP, nullable=True, default=None)
#     registered_on: Mapped[str] = mapped_column(
#         String(24),
#         nullable=False,
#         default=str(datetime.now().strftime("%d/%m/%Y, %H:%M")),
#     )
