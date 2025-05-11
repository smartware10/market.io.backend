from typing import Annotated, TYPE_CHECKING, List

from fastapi import APIRouter, Depends, status

from api.common import get_current_user
from api.dependencies import crud as crud_common
from core.models import Product as ProductModel
from core.helpers import db_helper
from core.schemas.product import (
    ProductCreate,
    ProductRead,
    ProductReadList,
    ProductUpdate,
    ProductUpdatePartial,
)

from api.dependencies.products import product_by_id
from . import crud

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.models import User as UserModel


router = APIRouter()


@router.get(
    "/",
    response_model=ProductReadList,
    status_code=status.HTTP_200_OK,
    name="products:get all products",
)
async def get_all_products(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ]
):
    return await crud_common.get_all_object(session=session, model=ProductModel)


@router.get(
    "/{product_id}/",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
)
async def get_product_by_id(
    product: Annotated[
        "ProductModel",
        Depends(product_by_id),
    ]
):
    return product


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    name="products:create a new product",
)
async def create_product(
    current_user: Annotated[
        "UserModel",
        get_current_user("v1", superuser=True),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    schema: ProductCreate,
):
    return await crud.create_product(
        session=session,
        product_in=schema,
    )


@router.put("/{product_id}")
async def update_product(
    current_user: Annotated[
        "UserModel",
        get_current_user("v1", superuser=True),
    ],
    product_update: ProductUpdate,
    product: Annotated[
        "ProductModel",
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
        "UserModel",
        get_current_user("v1", superuser=True),
    ],
    product_update: ProductUpdatePartial,
    product: Annotated[
        "ProductModel",
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
        "UserModel",
        get_current_user("v1", superuser=True),
    ],
    product: Annotated[
        "ProductModel",
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
