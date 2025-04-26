from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, field_validator

if TYPE_CHECKING:
    from .product import Product


class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

    @field_validator("parent_id", mode="before")
    def check_parent_category(cls, value):
        # Преобразуем значение в int, если оно строковое
        if value is not None:
            value = int(value)  # Преобразуем в int перед проверкой
            if value <= 0:
                raise ValueError("Parent category ID must be a positive integer.")
        return value


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryCreate):
    pass


class CategoryWithProduct(CategoryBase):
    products: Optional[list["Product"]] = None


class Category(CategoryBase):
    pass


class SubCategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    subcategories: Optional[list["Category"]] = None
