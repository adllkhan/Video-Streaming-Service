from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.auth.schemas import Token
from src.api.v1.auth.services import AuthService
from src.api.v1.auth.utils import create_access_token
from src.database import get_session

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    service = AuthService(session)
    user = await service.authenticate_user(form_data.username, form_data.password)
    token = create_access_token(data={"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}
