from typing import Annotated
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category
from core.helpers import db_helper


async def category_by_id(
    category_id: Annotated[int, Path(..., gt=0)],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> Category:
    category = await session.get(Category, category_id)
    if category:
        return category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Категория с ID: '{category_id}' не найдена.",
    )
