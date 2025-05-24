from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, RootModel


class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        ...,
        title="Product Name",
        description="Full name of the product",
        examples=["Samsung Galaxy A52 Smartphone"],
        max_length=128,
        min_length=3,
    )
    description: str = Field(
        ...,
        title="Description",
        description="Short description of the product",
        examples=["Modern smartphone with 6.5-inch screen"],
        max_length=512,
        min_length=3,
    )
    price: int = Field(
        ...,
        title="Price",
        description="Product price",
        examples=[19990],
        gt=0,
    )
    category_id: int = Field(
        ...,
        title="Category ID",
        description="ID of the category the product belongs to",
        examples=[3],
        gt=0,
    )


class ProductReadList(RootModel[List["ProductRead"]]):
    """Schema for reading a list of products"""

    pass


class ProductCreate(ProductBase):
    """Schema for creating a product"""

    pass


class ProductUpdate(ProductCreate):
    """Schema for updating a product"""

    pass


class ProductUpdatePartial(ProductBase):
    """Schema for partially updating a product"""

    name: Optional[str] = Field(
        default=None,
        title="Product Name",
        description="Full product name (optional)",
        examples=["Samsung Galaxy A52 Smartphone"],
        max_length=128,
        min_length=3,
    )
    description: Optional[str] = Field(
        default=None,
        title="Description",
        description="Short product description (optional)",
        examples=["Modern smartphone with 6.5-inch screen"],
        max_length=512,
        min_length=3,
    )
    price: Optional[int] = Field(
        default=None,
        title="Price",
        description="Product price in rubles (optional)",
        examples=[19990],
        gt=0,
    )
    category_id: Optional[int] = Field(
        default=None,
        title="Category ID",
        description="Category identifier (optional)",
        examples=[3],
        gt=0,
    )


class ProductRead(ProductBase):
    """Schema for reading a product"""

    id: int = Field(
        ...,
        title="Product ID",
        description="Unique identifier of the product",
        gt=0,
        examples=[101],
    )


from .category import CategoryReadWithProduct

ProductRead.model_rebuild()
