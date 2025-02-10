from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper
from . import crud
from .dependencies import product_by_id
from .schemas import ProductCreate, Product, ProductUpdate, ProductUpdatePartial

router = APIRouter(
    prefix=settings.api.v1.products,
    tags=["Products"],
)


@router.get(
    "/",
    response_model=list[Product],
    status_code=status.HTTP_200_OK,
)
async def get_products(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.get_products(session)


@router.get(
    "/{product_id}/",
    response_model=Product,
    status_code=status.HTTP_200_OK,
)
async def get_product_by_id(product: Product = Depends(product_by_id)):
    return product


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.create_product(session=session, product_in=product_in)


@router.put("/{product_id}")
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch("/{product_id}")
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
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
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await crud.delete_product(session=session, product=product)
