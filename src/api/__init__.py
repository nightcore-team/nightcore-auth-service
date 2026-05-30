from fastapi import APIRouter

from .routes import auth

# including routers to main api router
router = APIRouter(prefix="/auth")
router.include_router(auth.router)

__all__ = ["router"]
