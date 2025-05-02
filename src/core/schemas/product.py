from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, Field


class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        ...,
        title="Название товара",
        description="Полное название товара",
        examples=["Смартфон Samsung Galaxy A52"],
        max_length=128,
        min_length=3,
    )
    description: str = Field(
        ...,
        title="Описание",
        description="Краткое описание товара",
        examples=["Современный смартфон с экраном 6.5 дюйма"],
        max_length=512,
        min_length=3,
    )
    price: int = Field(
        ..., title="Цена", description="Цена товара в рублях", examples=[19990], gt=0
    )
    category_id: int = Field(
        ...,
        title="ID категории",
        description="Идентификатор категории, к которой относится товар",
        examples=[3],
        gt=0,
    )

    @field_validator("category_id", "price", mode="before")
    def check_category_id(cls, value):
        if value is not None:
            value = int(value)
            if value <= 0:
                raise ValueError("Price and CategoryID must be a positive integer.")
        return value


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(ProductBase):
    name: Optional[str] = Field(
        default=None,
        title="Название товара",
        description="Полное название товара (опционально)",
        examples=["Смартфон Samsung Galaxy A52"],
        max_length=128,
        min_length=3,
    )
    description: Optional[str] = Field(
        default=None,
        title="Описание",
        description="Краткое описание товара (опционально)",
        examples=["Современный смартфон с экраном 6.5 дюйма"],
        max_length=512,
        min_length=3,
    )
    price: Optional[int] = Field(
        default=None,
        title="Цена",
        description="Цена товара в рублях (опционально)",
        examples=[19990],
        gt=0,
    )
    category_id: Optional[int] = Field(
        default=None,
        title="ID категории",
        description="Идентификатор категории (опционально)",
        examples=[3],
        gt=0,
    )


class Product(ProductBase):
    id: int = Field(
        ...,
        title="ID товара",
        description="Уникальный идентификатор товара",
        gt=0,
        examples=[101],
    )
