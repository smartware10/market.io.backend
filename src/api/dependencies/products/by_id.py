from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status, Path

from api.api_v1.products import crud
from core.models import db_helper, Product

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def product_by_id(
    product_id: Annotated[int, Path],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
) -> Product:
    product = await crud.get_product_by_id(
        session=session,
        product_id=product_id,
    )
    if product:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product id: {product_id} not found.",
    )
