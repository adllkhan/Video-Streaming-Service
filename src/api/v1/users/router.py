from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from dependencies import get_current_user

from . import schemas
from .models import User
from .repositories import UserRepository
from .services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(path="", response_model=list[schemas.UsersOut])
async def get_users(
    session: AsyncSession = Depends(get_session),
) -> list[schemas.UsersOut]:
    repo = UserRepository(session=session)
    service = UserService(repository=repo)
    users = await service.get_users()
    return users


@router.get(path="/{user_id}", response_model=schemas.UserOut)
async def get_user(
    user_id: int, session: AsyncSession = Depends(get_session)
) -> schemas.UserOut:
    repo = UserRepository(session=session)
    service = UserService(repository=repo)
    user = await service.get_user(user_id=user_id)
    return user


@router.post(
    path="", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: schemas.UserIn, session: AsyncSession = Depends(get_session)
) -> schemas.UserOut:
    repo = UserRepository(session=session)
    service = UserService(repository=repo)
    user = await service.create_user(user=user)
    return user


@router.put(
    path="/me",
    response_model=schemas.UserOut,
    status_code=status.HTTP_205_RESET_CONTENT,
)
async def update_user(
    update: schemas.UserUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> schemas.UserOut:
    repo = UserRepository(session=session)
    service = UserService(repository=repo)
    user = await service.update_user(update=update, user=user)
    return user


@router.delete(
    path="/me",
    response_model=schemas.UserOut,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
) -> schemas.UserOut:
    repo = UserRepository(session=session)
    service = UserService(repository=repo)
    user = await service.delete_user(user=user)
    return user
