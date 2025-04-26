from typing import Type, List, TypeVar

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase)


async def get_all(session: AsyncSession, model: Type[T]) -> List[T]:
    stmt = select(model).order_by(model.id)
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return list(data)
