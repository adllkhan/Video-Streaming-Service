from database import get_session
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from .repositories import UserRepository
from .services import UserServices

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(path="", response_model=list[schemas.UsersOut])
async def get_users(
    session: AsyncSession = Depends(get_session),
) -> list[schemas.UsersOut]:
    repo = UserRepository(session=session)
    services = UserServices(repository=repo)
    users = await services.get_users()
    return users


@router.get(path="/{user_id}", response_model=schemas.UserOut)
async def get_user(
    user_id: int, session: AsyncSession = Depends(get_session)
) -> schemas.UserOut:
    repo = UserRepository(session=session)
    services = UserServices(repository=repo)
    user = await services.get_user(user_id=user_id)
    return user


@router.post(
    path="", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: schemas.UserIn, session: AsyncSession = Depends(get_session)
) -> schemas.UserOut:
    repo = UserRepository(session=session)
    services = UserServices(repository=repo)
    user = await services.create_user(user=user)
    return user


@router.put(
    path="/{user_id}",
    response_model=schemas.UserOut,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int, user: schemas.UserIn, session: AsyncSession = Depends(get_session)
) -> schemas.UserOut:
    repo = UserRepository(session=session)
    services = UserServices(repository=repo)
    user = await services.update_user(user_id=user_id, user=user)
    return user


@router.delete(
    path="/{user_id}",
    response_model=schemas.UserOut,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_id: int, session: AsyncSession = Depends(get_session)
) -> schemas.UserOut:
    repo = UserRepository(session=session)
    services = UserServices(repository=repo)
    user = await services.delete_user(user_id=user_id)
    return user
