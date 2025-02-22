"""  Create Read Update Delete """

from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import Category
from core.schemas.category import CategoryCreate


async def get_all_categories(session: AsyncSession) -> list[Category]:
    stmt = select(Category).order_by(Category.id)
    result: Result = await session.execute(stmt)
    categories = result.scalars().all()
    return list(categories)


async def get_category_with_subcategories(
    session: AsyncSession,
    category: Category,
):
    await session.refresh(category, ["subcategories"])
    return {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "subcategories": [
            {
                "id": sub.id,
                "name": sub.name,
                "description": sub.description,
            }
            for sub in category.subcategories
        ],
    }


async def get_category_by_id(
    session: AsyncSession,
    category_id: int,
) -> Optional[Category]:
    return await session.get(Category, category_id)


async def create_category(
    session: AsyncSession,
    schema_create: CategoryCreate,
) -> Category:
    # Если parent_id передан, проверяем существование родительской категории
    if schema_create.parent_id:
        parent_category = await session.execute(
            select(Category).filter(Category.id == schema_create.parent_id)
        )
        parent_category = parent_category.scalar_one_or_none()
        if not parent_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Parent category with id {schema_create.parent_id} does not exist.",
            )

    # Проверка, существует ли категория с таким же названием
    existing_category = await session.execute(
        select(Category).filter(Category.name == schema_create.name)
    )
    existing_category = existing_category.scalar_one_or_none()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{schema_create.name}' already exists.",
        )

    # Создание новой категории
    category = Category(**schema_create.model_dump())
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
