from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user, get_session
from models import User
from repositories import UserRepository
from schemas.users import UserInSchema, UserOutSchema, UserUpdateSchema
from services.users import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(path="", response_model=list[UserOutSchema])
async def get_users(
    session: AsyncSession = Depends(get_session),
) -> list[UserOutSchema]:
    repo = UserRepository(session=session)
    service = UserService(repository=repo)
    return await service.get_users()


@router.get(path="/{user_id}", response_model=UserOutSchema)
async def get_user(
    user_id: int, session: AsyncSession = Depends(get_session)
) -> UserOutSchema:
    repo = UserRepository(session=session)
    service = UserService(repository=repo)
    return await service.get_user(user_id=user_id)


@router.post(path="", response_model=UserOutSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserInSchema, session: AsyncSession = Depends(get_session)
) -> UserOutSchema:
    repo = UserRepository(session=session)
    service = UserService(repository=repo)
    return await service.create_user(user=user)


@router.put(
    path="/me",
    response_model=UserOutSchema,
)
async def update_user(
    update: UserUpdateSchema,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> UserOutSchema:
    repo = UserRepository(session=session)
    service = UserService(repository=repo)
    return await service.update_user(update=update, user=user)


@router.delete(
    path="/me",
    response_model=UserOutSchema,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
) -> UserOutSchema:
    repo = UserRepository(session=session)
    service = UserService(repository=repo)
    return await service.delete_user(user=user)
