from typing import Optional, TYPE_CHECKING, List
from pydantic import BaseModel, RootModel, ConfigDict, Field

if TYPE_CHECKING:
    from .product import ProductRead


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


class CategoryReadList(RootModel[List["CategoryRead"]]):
    """Схема для чтения списка категорий"""

    pass


class CategoryReadListWithProducts(RootModel[List["CategoryReadWithProduct"]]):
    """Схема для чтения списка категорий с продуктами"""

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
        examples=[3],
        gt=0,
    )


class SubCategoryBase(CategoryRead):
    """Схема для чтения подкатегорий выбраной категории"""

    subcategories: Optional[List["CategoryRead"]] = Field(
        default=None,
        title="Подкатегории",
        description="Список вложенных подкатегорий (если есть).",
    )


class CategoryReadWithProduct(CategoryRead):
    """Схема для чтения категории со списком продуктов"""

    products: Optional[List["ProductRead"]] = Field(
        default=None,
        title="Продукты категории",
        description="Список продуктов, связанных с этой категорией.",
    )


from .product import ProductRead

CategoryReadWithProduct.model_rebuild()
