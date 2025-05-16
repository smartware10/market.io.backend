from typing import Annotated, TYPE_CHECKING

from fastapi import (
    APIRouter,
    Depends,
    Response,
    HTTPException,
)
from starlette import status

from api.common import get_current_user
from api.dependencies import crud as common_crud
from core.helpers import db_helper
from core.models import Category as CategoryModel
from core.schemas.category import (
    CategoryRead,
    CategoryReadList,
    CategoryReadListWithProducts,
    CategoryCreate,
    SubCategoryBase,
)

from api.dependencies.categories import category_by_id
from . import crud

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.models import User as UserModel

router = APIRouter()


@router.get(
    "/",
    response_model=CategoryReadList,
    status_code=status.HTTP_200_OK,
    name="categories:get all categories",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "There are no categories",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
        },
    },
)
async def get_all_categories(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    try:
        categories = await common_crud.get_all_object(
            session=session,
            model=CategoryModel,
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    if not categories:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return categories


@router.get(
    "/all/",
    response_model=CategoryReadListWithProducts,
    status_code=status.HTTP_200_OK,
    name="categories:get all categories with products",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "There are no categories",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
        },
    },
)
async def get_all_categories_with_products(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await crud.get_all_categories_with_products(session=session)


@router.get(
    "/{category_id}/",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
    name="categories:get category by id",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The category does not exist",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
        },
    },
)
async def get_category_by_id(
    category: Annotated[
        "CategoryModel",
        Depends(category_by_id),
    ],
):
    return category


@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    name="categories:create a new category",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "examples": {
                        "Error creating new category.": {
                            "summary": "Error creating new category.",
                            "value": {
                                "detail": {
                                    "code": "INTEGRITY_ERROR",
                                    "reason": "Error creating new category.",
                                },
                            },
                        },
                        "Parent category with ID does not exist.": {
                            "summary": "ID does not exist.",
                            "value": {
                                "detail": {
                                    "code": "PARENT_ID_DOES_NOT_EXIST",
                                    "reason": "Parent category with ID does not exist.",
                                }
                            },
                        },
                    }
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Category already exists",
            "content": {
                "application/json": {
                    "examples": {
                        "A category with the name already exists.": {
                            "summary": "Name already exists.",
                            "value": {
                                "detail": {
                                    "code": "NAME_ALREADY_EXISTS",
                                    "reason": "A category with the name already exists.",
                                }
                            },
                        },
                    }
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
        },
    },
)
async def create_category(
    current_user: Annotated[
        "UserModel",
        get_current_user("v1", superuser=True),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    schema: CategoryCreate,
):
    return await crud.create_category(
        session=session,
        category_in=schema,
    )


@router.get(
    "/sub/{category_id}/",
    response_model=SubCategoryBase,
    status_code=status.HTTP_200_OK,
    name="categories:get category with subcategories",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The category does not exist",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
        },
    },
)
async def get_category_with_subcategories(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    category: Annotated[
        "CategoryModel",
        Depends(category_by_id),
    ],
):
    return await crud.get_category_with_subcategories(
        session=session,
        category=category,
    )
