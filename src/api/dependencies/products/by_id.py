from typing import Annotated
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.helpers import db_helper


async def product_by_id(
    product_id: Annotated[int, Path(..., gt=0)],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> Product:
    product = await session.get(Product, product_id)
    if product:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product ID: '{product_id}' was not found.",
    )
