from typing import Optional, TYPE_CHECKING, List
from pydantic import BaseModel, RootModel, ConfigDict, Field

if TYPE_CHECKING:
    from .product import ProductRead


class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        ...,
        title="Category Name",
        min_length=3,
        max_length=32,
        description="Unique category name, between 3 and 32 characters.",
        examples=["Electronics"],
    )
    description: Optional[str] = Field(
        default=None,
        title="Category Description",
        max_length=128,
        description="A short description of the category (optional), between 3 and 128 characters.",
        examples=["Products in the field of electronics"],
    )
    parent_id: Optional[int] = Field(
        default=None,
        gt=0,
        title="Parent Category ID",
        description="ID of the parent category, if this is a subcategory.",
        examples=[1],
    )


class CategoryReadList(RootModel[List["CategoryRead"]]):
    """Schema for reading a list of categories"""

    pass


class CategoryReadListWithProducts(RootModel[List["CategoryReadWithProduct"]]):
    """Schema for reading a list of categories with products"""

    pass


class CategoryCreate(CategoryBase):
    """Schema for creating a category"""

    pass


class CategoryUpdate(CategoryCreate):
    """Schema for updating a category"""

    pass


class CategoryRead(CategoryBase):
    """Schema for reading a category"""

    id: int = Field(
        ...,
        title="Category ID",
        description="Unique identifier of the category.",
        examples=[3],
        gt=0,
    )


class SubCategoryBase(CategoryRead):
    """Schema for reading subcategories of a selected category"""

    subcategories: Optional[List["CategoryRead"]] = Field(
        default=None,
        title="Subcategories",
        description="List of nested subcategories (if any).",
    )


class CategoryReadWithProduct(CategoryRead):
    """Schema for reading a category with a list of products"""

    products: Optional[List["ProductRead"]] = Field(
        default=None,
        title="Category Products",
        description="List of products associated with this category.",
    )


from .product import ProductRead

CategoryReadWithProduct.model_rebuild()
