"""Create Read Update Delete"""

from typing import List

from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from core.models import Category
from core.schemas.category import CategoryCreate, SubCategoryBase


async def get_all_categories_with_products(session: AsyncSession) -> List[Category]:
    stmt = (
        select(Category).options(selectinload(Category.products)).order_by(Category.id)
    )
    result: Result = await session.execute(stmt)
    categories = result.scalars().all()
    return list(categories)


async def get_category_with_subcategories(
    session: AsyncSession,
    category: Category,
) -> SubCategoryBase:
    stmt = (
        select(Category)
        .options(selectinload(Category.subcategories))
        .where(Category.id == category.id)
    )
    result = await session.execute(stmt)
    category_with_subs = result.scalar_one()
    return SubCategoryBase.model_validate(category_with_subs)


async def create_category(
    session: AsyncSession,
    category_in: CategoryCreate,
) -> Category:
    # If 'parent_id' is passed, check for the existence of the parent category
    if category_in.parent_id:
        parent_category = await session.execute(
            select(Category).filter(Category.id == category_in.parent_id)
        )
        parent_category = parent_category.scalar_one_or_none()
        if not parent_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "PARENT_ID_DOES_NOT_EXIST",
                    "reason": f"Parent category with ID: '{category_in.parent_id}' does not exist.",
                },
            )

    # Check if a category with the same name exists
    existing_category = await session.execute(
        select(Category).filter(Category.name == category_in.name)
    )
    existing_category = existing_category.scalar_one_or_none()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "NAME_ALREADY_EXISTS",
                "reason": f"A category with the name '{category_in.name}' already exists.",
            },
        )

    # Create a new category
    category = Category(**category_in.model_dump())
    session.add(category)
    try:
        await session.commit()
        await session.refresh(category)
    except IntegrityError:
        # Catch an error if unique constraints are not met
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INTEGRITY_ERROR",
                "reason": "Error creating new category.",
            },
        )

    return category
