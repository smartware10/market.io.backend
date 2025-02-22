from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .product import Product


class Category(Base, IdIntPkMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(128))

    parent_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
    )
    parent: Mapped["Category"] = relationship(
        "Category",
        remote_side="Category.id",
        backref="subcategories",
    )

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete",
    )

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, parent_id={self.parent_id})"
