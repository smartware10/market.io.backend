from typing import Annotated
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category
from core.helpers import db_helper


async def category_by_id(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    category_id: Annotated[int, Path(..., gt=0)],
) -> Category:
    category = await session.get(Category, category_id)
    if category:
        return category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category id: {category_id} not found.",
    )
