"""Lifespan event handler for the API."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from src.core.config._global import config
from src.infrastructure.redis.client import create_redis_client

if TYPE_CHECKING:
    from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: "FastAPI") -> AsyncGenerator[None]:
    """Lifespan event handler for the API."""
    app.state.config = config

    redis_client = create_redis_client(config.redis)
    app.state.redis_client = redis_client

    yield

    await redis_client.aclose()
