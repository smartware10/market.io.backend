from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.schemas.category import Category


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(ProductCreate):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    category_id: Optional[int] = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    category: Optional[Category]
    id: int
