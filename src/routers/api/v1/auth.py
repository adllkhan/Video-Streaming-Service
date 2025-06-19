from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session
from repositories import UserRepository
from schemas.auth import CredentialsInSchema, TokenOutSchema
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenOutSchema)
async def login(
    credentials: CredentialsInSchema, session: AsyncSession = Depends(get_session)
) -> TokenOutSchema:
    repo = UserRepository(session=session)
    service = AuthService(repository=repo)
    return await service.login(credentials=credentials)
