"""Main application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_router
from src.api.events.exceptions import EXCEPTION_HANDLERS
from src.api.events.lifespan import lifespan


def main() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(lifespan=lifespan)
    app.include_router(api_router)
    app.exception_handlers.update(EXCEPTION_HANDLERS)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
