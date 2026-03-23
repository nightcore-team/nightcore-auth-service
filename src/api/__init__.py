from fastapi import APIRouter

from .routes import auth

# including routers to main api router
router = APIRouter(prefix="/api")
router.include_router(auth.router, prefix="/auth", tags=["authentication"])

__all__ = ["router"]
