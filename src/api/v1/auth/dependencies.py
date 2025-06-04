from fastapi import Depends, HTTPException
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.auth.config import oauth2_scheme
from src.api.v1.auth.utils import decode_access_token
from src.api.v1.users.repositories import UserRepository
from src.database import get_session


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
):
    try:
        payload = decode_access_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await UserRepository(session).get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
