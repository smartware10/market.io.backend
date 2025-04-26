from typing import Annotated, TYPE_CHECKING, List

from fastapi import APIRouter, Depends
from starlette import status

from api.common import get_current_user
from api.dependencies import crud as common_crud
from core.helpers import db_helper
from core.models import Category as CategoryModel
from core.schemas.category import (
    Category,
    CategoryWithProduct,
    CategoryCreate,
    SubCategoryBase,
)

from api.dependencies.categories import category_by_id
from . import crud

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.models import User

router = APIRouter()


@router.get(
    "/",
    response_model=List[Category],
    status_code=status.HTTP_200_OK,
    name="categories:get all categories",
)
async def get_all_categories(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ]
):
    return await common_crud.get_all(session=session, model=CategoryModel)


@router.get(
    "/all/",
    response_model=list[CategoryWithProduct],
    status_code=status.HTTP_200_OK,
    name="categories:get all categories with products",
)
async def get_all_categories_with_products(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ]
):
    return await crud.get_all_categories_with_products(session=session)


@router.get(
    "/{category_id}/",
    response_model=Category,
    status_code=status.HTTP_200_OK,
    name="categories:get category by id",
)
async def get_category_by_id(
    category: Annotated[
        "Category",
        Depends(category_by_id),
    ]
):
    return category


@router.post(
    "/",
    response_model=Category,
    status_code=status.HTTP_201_CREATED,
    name="categories:create a new category",
)
async def add_category(
    current_user: Annotated[
        "User",
        get_current_user("v1", superuser=True),
    ],
    schema: CategoryCreate,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await crud.create_category(
        session=session,
        schema_create=schema,
    )


@router.get(
    "/sub/{category_id}/",
    response_model=SubCategoryBase,
    status_code=status.HTTP_200_OK,
    name="categories:get category with subcategories",
)
async def get_category_with_subcategories(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    category: Annotated[
        "Category",
        Depends(category_by_id),
    ],
):
    return await crud.get_category_with_subcategories(
        session=session,
        category=category,
    )
