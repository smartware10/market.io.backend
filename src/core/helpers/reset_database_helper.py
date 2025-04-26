from sqlalchemy import text

from core.models import Base
from core.logger import logger as log
from . import db_helper


async def reset_database_helper() -> None:
    async for session in db_helper.session_getter():
        async with session.begin():
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(table.delete())
                log.info("Reset table %s successful", table)

            for table in Base.metadata.tables.keys():
                sequence_name = f"{table}_id_seq"
                # Перевіримо чи існує sequence перед ALTER
                result = await session.execute(
                    text(
                        """
                         SELECT 1
                         FROM pg_class
                         WHERE relkind = 'S' AND relname = :seq_name
                         """
                    ),
                    {"seq_name": sequence_name},
                )
                exists = result.scalar()
                if exists:
                    await session.execute(
                        text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1")
                    )

            await session.commit()
