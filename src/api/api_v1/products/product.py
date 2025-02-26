from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends, status

from core.models import db_helper
from core.schemas.product import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)

from api.api_v1.auth.fastapi_users_router import current_active_superuser
from api.dependencies.products import product_by_id
from . import crud

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.models import User


router = APIRouter()


@router.get(
    "/",
    response_model=list[Product],
    status_code=status.HTTP_200_OK,
)
async def get_products(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ]
):
    return await crud.get_products(session=session)


@router.get(
    "/{product_id}/",
    response_model=Product,
    status_code=status.HTTP_200_OK,
)
async def get_product_by_id(
    product: Annotated[
        "Product",
        Depends(product_by_id),
    ]
):
    return product


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    current_user: Annotated[
        "User",
        Depends(current_active_superuser),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    product_in: ProductCreate,
):
    return await crud.create_product(
        session=session,
        product_in=product_in,
    )


@router.put("/{product_id}")
async def update_product(
    current_user: Annotated[
        "User",
        Depends(current_active_superuser),
    ],
    product_update: ProductUpdate,
    product: Annotated[
        "Product",
        Depends(product_by_id),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch("/{product_id}")
async def update_product_partial(
    current_user: Annotated[
        "User",
        Depends(current_active_superuser),
    ],
    product_update: ProductUpdatePartial,
    product: Annotated[
        "Product",
        Depends(product_by_id),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    current_user: Annotated[
        "User",
        Depends(current_active_superuser),
    ],
    product: Annotated[
        "Product",
        Depends(product_by_id),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
) -> None:
    await crud.delete_product(
        session=session,
        product=product,
    )
