from fastapi import APIRouter

from .users import UserRepository
from .users import router as users_router

router = APIRouter(prefix="/v1")
router.include_router(router=users_router)

__all__ = ["router", "UserRepository"]
