from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: int
    category_id: int

    @field_validator("category_id", "price", mode="before")
    def check_category_id(cls, value):
        # Преобразуем значение в int, если оно строковое
        if value is not None:
            value = int(value)  # Преобразуем в int перед проверкой
            if value <= 0:
                raise ValueError("Price and CategoryID must be a positive integer.")
        return value


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
    pass
