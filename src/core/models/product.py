from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .category import Category

    # from .order import Order
#     from .order_product_association import OrderProductAssociation


class Product(Base, IdIntPkMixin):

    name: Mapped[str] = mapped_column(String(128), index=True)
    description: Mapped[str] = mapped_column(String(512))
    price: Mapped[int] = mapped_column(Integer, index=True)

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "categories.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
        lazy="joined",
    )

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, description={self.description}, price={self.price}, category_id={self.category_id})"

    # secondary
    # orders: Mapped[list["Order"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="products"
    # )

    # association between Order -> OrderProductAssociation -> Product
    # orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
    #     back_populates="product",
    # )
