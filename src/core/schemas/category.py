from typing import Optional, TYPE_CHECKING, List
from pydantic import BaseModel, RootModel, ConfigDict, field_validator, Field

if TYPE_CHECKING:
    from .product import Product


class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        ...,
        title="Название категории",
        min_length=3,
        max_length=32,
        description="Уникальное название категории, от 3 до 32 символов.",
        examples=["Электроника"],
    )
    description: Optional[str] = Field(
        default=None,
        title="Описание категории",
        max_length=128,
        description="Краткое описание категории (необязательно), от 3 до 128 символов.",
        examples=["Товары из области электроники"],
    )
    parent_id: Optional[int] = Field(
        default=None,
        gt=0,
        title="ID родительской категории",
        description="ID родительской категории, если эта категория является подкатегорией.",
        examples=[1],
    )

    @field_validator("parent_id", mode="before")
    def check_parent_category(cls, value):
        # Преобразуем значение в int, если оно строковое
        if value is not None:
            value = int(value)
            if value <= 0:
                raise ValueError(
                    "ID родительской категории должен быть положительным числом."
                )
        return value


class CategoryReadList(RootModel[List["CategoryRead"]]):
    pass


class CategoryReadListWithProducts(RootModel[List["CategoryReadWithProduct"]]):
    pass


class CategoryCreate(CategoryBase):
    """Схема для создания категории"""

    pass


class CategoryUpdate(CategoryCreate):
    """Схема для обновления категории"""

    pass


class CategoryRead(CategoryBase):
    """Схема для чтения категории"""

    id: int = Field(
        ...,
        title="ID категории",
        description="Уникальный идентификатор категории.",
        examples=[5],
        gt=0,
    )


class SubCategoryBase(CategoryRead):
    subcategories: Optional[List["CategoryRead"]] = Field(
        default=None,
        title="Подкатегории",
        description="Список вложенных подкатегорий (если есть).",
    )


class CategoryReadWithProduct(CategoryRead):
    products: Optional[List["Product"]] = Field(
        default=None,
        title="Продукты категории",
        description="Список продуктов, связанных с этой категорией.",
    )
