from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends
from starlette import status

from core.models import db_helper
from core.schemas.category import Category, CategoryCreate, SubCategoryBase

from api.dependencies.categories import category_by_id
from api.api_v1.auth.fastapi_users_router import current_active_superuser
from . import crud

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.models import User

router = APIRouter()


@router.get(
    "/",
    response_model=list[Category],
    status_code=status.HTTP_200_OK,
    name="categories:get all categories",
)
async def get_all_categories(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ]
):
    return await crud.get_all_categories(session=session)


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
        Depends(current_active_superuser),
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
