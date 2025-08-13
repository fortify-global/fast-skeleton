"""
[TODO][WIP] DO not rely to this yet
Async PostgreSQL access utilities: connection and query helpers.

This module provides two classes:
- PostgresConnection: manages a reusable asyncpg pool (singleton-like)
- PostgresQuery: convenience query helpers that reuse the shared pool
"""

from __future__ import annotations

import asyncio
import traceback
import os
from typing import Any, Optional

import asyncpg
from app import logger
from app.error.exception import DatabaseException

"""
Manage a shared asyncpg pool across the application.

The first call to init_pool creates the pool; subsequent calls reuse it.
"""

class PGSinglePool:
    # Class-level configuration (single pool per process)
    HOST: str = os.getenv("PGHOST", "127.0.0.1")
    PORT: str = os.getenv("PGPORT", "5432")
    USER: str = os.getenv("PGUSER", "postgres")
    PASSWORD: str = os.getenv("PGPASSWORD", "postgres")
    DATABASE: str = os.getenv("PGDATABASE", "postgres")

    _pool: Optional[asyncpg.Pool] = None
    _pool_lock: asyncio.Lock = asyncio.Lock()

    @classmethod
    def build_dsn(cls) -> str:
        return f"postgresql://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DATABASE}"

    @classmethod
    async def init_pool(
        cls,
        dsn: Optional[str] = None,
        *,
        min_size: int = 1,
        max_size: int = 10,
        timeout: float = 10.0,
        **connect_kwargs: Any,
    ) -> asyncpg.Pool:
        if cls._pool is not None:
            return cls._pool

        async with cls._pool_lock:
            if cls._pool is not None:
                return cls._pool
            dsn = dsn or cls.build_dsn()
            logger.info(f"Creating PostgreSQL pool postgresql://{cls.USER}:******@{cls.HOST}:{cls.PORT}/{cls.DATABASE}")
            try:
                cls._pool = await asyncpg.create_pool(
                    dsn=dsn,
                    min_size=min_size,
                    max_size=max_size,
                    timeout=timeout,
                    **connect_kwargs,
                )
            except Exception as exc:
                logger.exception(f"Failed to initialize PostgreSQL pool postgresql://{cls.USER}:******@{cls.HOST}:{cls.PORT}/{cls.DATABASE}")
                raise DatabaseException(
                    code=500,
                    key='database_connection_error',
                    reason="Failed to initialize PostgreSQL pool",
                    detail={"trace": "".join(traceback.format_exc())},
                ) from exc
            return cls._pool

    @classmethod
    async def get_pool(cls) -> asyncpg.Pool:
        if cls._pool is None:
            return await cls.init_pool()
        return cls._pool

    @classmethod
    async def close_pool(cls) -> None:
        if cls._pool is not None:
            logger.info("Closing PostgreSQL pool")
            await cls._pool.close()
            cls._pool = None


class PostgresQuery:
    @staticmethod
    async def fetchrow(query: str, *args: Any) -> Optional[asyncpg.Record]:
        try:
            pool = await PGSinglePool.get_pool()
            async with pool.acquire() as conn:
                return await conn.fetchrow(query, *args)
        except Exception as exc:
            logger.exception("postgres.fetchrow failed")
            raise DatabaseException(
                code=500,
                key='database_error',
                reason="Database fetchrow failed",
                detail={"query": query, "args": args, "trace": "".join(traceback.format_exc())},
            ) from exc


class PGMultiPool:
    _pools: dict[str, asyncpg.Pool] = {}
    _locks: dict[str, asyncio.Lock] = {}

    @classmethod
    def _get_lock(cls, client_key: str) -> asyncio.Lock:
        lock = cls._locks.get(client_key)
        if lock is None:
            lock = asyncio.Lock()
            cls._locks[client_key] = lock
        return lock

    @staticmethod
    def build_dsn(*, dsn: Optional[str] = None, host: Optional[str] = None, port: Optional[str] = None,
                  user: Optional[str] = None, password: Optional[str] = None, database: Optional[str] = None) -> str:
        if dsn:
            return dsn
        host = host or os.getenv("PGHOST", "127.0.0.1")
        port = port or os.getenv("PGPORT", "5432")
        user = user or os.getenv("PGUSER", "postgres")
        password = password or os.getenv("PGPASSWORD", "postgres")
        database = database or os.getenv("PGDATABASE", "postgres")
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

    @classmethod
    async def init_pool_for(
        cls,
        client_key: str,
        *,
        dsn: Optional[str] = None,
        min_size: int = 1,
        max_size: int = 10,
        timeout: float = 10.0,
        host: Optional[str] = None,
        port: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        **connect_kwargs: Any,
    ) -> asyncpg.Pool:
        if client_key in cls._pools:
            return cls._pools[client_key]

        lock = cls._get_lock(client_key)
        async with lock:
            if client_key in cls._pools:
                return cls._pools[client_key]

            final_dsn = cls.build_dsn(
                dsn=dsn, host=host, port=port, user=user, password=password, database=database
            )
            # Mask password in logs
            try:
                masked = final_dsn
                if "://" in masked and "@" in masked:
                    head, tail = masked.split("://", 1)
                    creds, rest = tail.split("@", 1)
                    if ":" in creds:
                        u, _p = creds.split(":", 1)
                        masked = f"{head}://{u}:******@{rest}"
            except Exception:
                masked = "postgresql://***"

            logger.info("Creating PostgreSQL pool for tenant %s -> %s", client_key, masked)
            try:
                pool = await asyncpg.create_pool(
                    dsn=final_dsn,
                    min_size=min_size,
                    max_size=max_size,
                    timeout=timeout,
                    **connect_kwargs,
                )
            except Exception as exc:
                logger.exception("Failed to initialize PostgreSQL pool for tenant %s", client_key)
                raise DatabaseException(
                    code=500,
                    key='database_connection_error',
                    reason=f"Failed to initialize pool for tenant {client_key}",
                    detail={"dsn": masked, "trace": "".join(traceback.format_exc())},
                ) from exc
            cls._pools[client_key] = pool
            return pool

    @classmethod
    async def get_pool_for(cls, client_key: str) -> asyncpg.Pool:
        pool = cls._pools.get(client_key)
        if pool is None:
            raise DatabaseException(
                code=500,
                key='database_connection_error',
                reason=f"Pool for tenant {client_key} is not initialized",
                detail=None,
            )
        return pool

    @classmethod
    async def close_pool_for(cls, client_key: str) -> None:
        pool = cls._pools.pop(client_key, None)
        if pool is not None:
            await pool.close()

    @classmethod
    async def close_all(cls) -> None:
        for key, pool in list(cls._pools.items()):
            try:
                await pool.close()
            finally:
                cls._pools.pop(key, None)


class PGMultiQuery:
    @staticmethod
    async def fetchrow(client_key: str, query: str, *args: Any) -> Optional[asyncpg.Record]:
        try:
            pool = await PGMultiPool.get_pool_for(client_key)
            async with pool.acquire() as conn:
                return await conn.fetchrow(query, *args)
        except Exception as exc:
            logger.exception("postgres(fetchrow) failed for tenant %s", client_key)
            raise DatabaseException(
                code=500,
                key='database_error',
                reason="Database fetchrow failed",
                detail={"tenant": client_key, "query": query, "args": args, "trace": "".join(traceback.format_exc())},
            ) from exc

    @staticmethod
    async def fetch(client_key: str, query: str, *args: Any) -> list[asyncpg.Record]:
        try:
            pool = await PGMultiPool.get_pool_for(client_key)
            async with pool.acquire() as conn:
                rows = await conn.fetch(query, *args)
                return rows
        except Exception as exc:
            logger.exception("postgres(fetch) failed for tenant %s", client_key)
            raise DatabaseException(
                code=500,
                key='database_error',
                reason="Database fetch failed",
                detail={"tenant": client_key, "query": query, "args": args, "trace": "".join(traceback.format_exc())},
            ) from exc

    @staticmethod
    async def execute(client_key: str, query: str, *args: Any) -> str:
        try:
            pool = await PGMultiPool.get_pool_for(client_key)
            async with pool.acquire() as conn:
                return await conn.execute(query, *args)
        except Exception as exc:
            logger.exception("postgres(execute) failed for tenant %s", client_key)
            raise DatabaseException(
                code=500,
                key='database_error',
                reason="Database execute failed",
                detail={"tenant": client_key, "query": query, "args": args, "trace": "".join(traceback.format_exc())},
            ) from exc
