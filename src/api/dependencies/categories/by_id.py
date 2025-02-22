from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException, status, Path

from api.api_v1.categories import crud
from core.models import db_helper, Category

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def category_by_id(
    category_id: Annotated[int, Path],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
) -> Category:
    category = await crud.get_category_by_id(
        session=session,
        category_id=category_id,
    )
    if category:
        return category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category id: {category_id} not found.",
    )
