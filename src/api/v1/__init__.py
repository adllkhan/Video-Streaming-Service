from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router

router = APIRouter(prefix="/v1")
router.include_router(router=auth_router)
router.include_router(router=users_router)
