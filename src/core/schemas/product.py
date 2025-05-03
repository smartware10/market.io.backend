from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, RootModel


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
        ..., title="Цена", description="Цена товара", examples=[19990], gt=0
    )
    category_id: int = Field(
        ...,
        title="ID категории",
        description="Идентификатор категории, к которой относится товар",
        examples=[3],
        gt=0,
    )


class ProductReadList(RootModel[List["ProductRead"]]):
    """Схема для чтения списка продуктов"""

    pass


class ProductCreate(ProductBase):
    """Схема для создания продукта"""

    pass


class ProductUpdate(ProductCreate):
    """Схема для обновления продукта"""

    pass


class ProductUpdatePartial(ProductBase):
    """Схема для частичного обновления продукта"""

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


class ProductRead(ProductBase):
    """Схема для чтения продукта"""

    id: int = Field(
        ...,
        title="ID товара",
        description="Уникальный идентификатор товара",
        gt=0,
        examples=[101],
    )


from .category import CategoryReadWithProduct

ProductRead.model_rebuild()
