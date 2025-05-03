from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .product import Product


class Category(Base, IdIntPkMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
    )

    # Отношение к родительской категории
    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        remote_side="Category.id",
        back_populates="subcategories",
    )

    # Список подкатегорий
    subcategories: Mapped[List["Category"]] = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    # Продукты, связанные с категорией
    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, description={self.description}, parent_id={self.parent_id})"
