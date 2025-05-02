"""  Create Read Update Delete """

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
    await session.refresh(category, ["subcategories"])
    return SubCategoryBase.model_validate(category)


async def create_category(
    session: AsyncSession,
    category_in: CategoryCreate,
) -> Category:
    # Если parent_id передан, проверяем существование родительской категории
    if category_in.parent_id:
        parent_category = await session.execute(
            select(Category).filter(Category.id == category_in.parent_id)
        )
        parent_category = parent_category.scalar_one_or_none()
        if not parent_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Parent category with id {category_in.parent_id} does not exist.",
            )

    # Проверка, существует ли категория с таким же названием
    existing_category = await session.execute(
        select(Category).filter(Category.name == category_in.name)
    )
    existing_category = existing_category.scalar_one_or_none()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{category_in.name}' already exists.",
        )

    # Создание новой категории
    category = Category(**category_in.model_dump())
    session.add(category)
    try:
        await session.commit()
        await session.refresh(category)
    except IntegrityError:
        # Ловим ошибку, если уникальные ограничения не выполнены
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while saving category.",
        )

    return category
