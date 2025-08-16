from typing import Optional

import asyncpg
from app.error.exception import DatabaseException
from app.util.postgres import PGSinglePool

from pydantic import BaseModel


class DbHealth(BaseModel):
    ok: bool
    server_version: str = ''


class HealthResponse(BaseModel):
    status: str
    version: str
    message: str


async def get_db_health() -> DbHealth:
    pool: asyncpg.Pool = await PGSinglePool.get_pool()
    query = 'SHOW server_version'
    try:
        async with pool.acquire() as conn:
            version: Optional[str] = await conn.fetchval(query)
            return DbHealth(ok=True, server_version=str(version) if version else None)
    except Exception:
        raise DatabaseException(code=500, key='query_error', reason=query)
