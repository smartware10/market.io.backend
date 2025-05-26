"""Create Read Update Delete"""

from typing import List

from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from core.models import Product, Category
from core.schemas.product import ProductCreate, ProductUpdate, ProductUpdatePartial


async def get_products(session: AsyncSession) -> List[Product]:
    stmt = select(Product).options(joinedload(Product.category)).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def create_product(
    session: AsyncSession,
    product_in: ProductCreate,
) -> Product:
    # If 'category_id' is passed, check for the existence of the category
    category = await session.get(Category, product_in.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID: '{product_in.category_id}' not found.",
        )

    # Creation of a new product
    product = Product(**product_in.model_dump())
    session.add(product)
    try:
        await session.commit()
        await session.refresh(product)
    except IntegrityError:
        # Catch an error if unique constraints are not met
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating new product.",
        )

    return product


async def update_product(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> Product:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: Product) -> None:
    await session.delete(product)
    await session.commit()
