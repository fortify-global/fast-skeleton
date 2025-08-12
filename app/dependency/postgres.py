"""
[TODO] Work in progress. Would like to have a connection class that can used by everyone to 
query database and get response
USer should be able to get_connection and query.
"""
from __future__ import annotations

import asyncio
import os
from typing import Any, Optional

import asyncpg
from app import logger

_database_url: Optional[str] = None
_pool: Optional[asyncpg.Pool] = None
_pool_lock = asyncio.Lock()


def build_dsn() -> str:
    global _database_url
    host = os.getenv("PGHOST", "127.0.0.1")
    port = os.getenv("PGPORT", "5432")
    user = os.getenv("PGUSER", "postgres")
    password = os.getenv("PGPASSWORD", "postgres")
    database = os.getenv("PGDATABASE", "postgres")
    _database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    return _database_url


async def init_pool(
    dsn: Optional[str] = None,
    *,
    min_size: int = 1,
    max_size: int = 10,
    timeout: float = 10.0,
    **connect_kwargs: Any,
) -> asyncpg.Pool:
    global _pool
    if _pool is not None:
        return _pool

    async with _pool_lock:
        if _pool is not None:
            return _pool
        dsn  = build_dsn()
        logger.info("Creating PostgreSQL pool to %s", dsn)
        _pool = await asyncpg.create_pool(
            dsn=dsn,
            min_size=min_size,
            max_size=max_size,
            timeout=timeout,
            **connect_kwargs,
        )
        return _pool


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        return await init_pool()
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        logger.info("Closing PostgreSQL pool")
        await _pool.close()
        _pool = None


# Convenience query helpers

async def fetchval(query: str, *args: Any) -> Any:
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchval(query, *args)


async def fetchrow(query: str, *args: Any) -> Optional[asyncpg.Record]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, *args)


async def fetch(query: str, *args: Any) -> list[asyncpg.Record]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *args)
        return list(rows)


async def execute(query: str, *args: Any) -> str:
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)