from typing import TYPE_CHECKING, Annotated, Type
from fastapi import Depends, HTTPException, status, Path

from core.models import Category
from core.helpers import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def category_by_id(
    category_id: Annotated[int, Path],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
) -> Type[Category]:
    category = await session.get(Category, category_id)
    if category:
        return category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category id: {category_id} not found.",
    )
