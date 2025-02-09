from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .order import Order
    from .order_product_association import OrderProductAssociation


class Product(IdIntPkMixin, Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    # secondary
    # orders: Mapped[list["Order"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="products"
    # )

    # association between Order -> OrderProductAssociation -> Product
    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",
    )
