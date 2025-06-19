from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from core.config import auth_config as config
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain, hashed)


def create_access_token(
    user: User, expires_delta: int = config.ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    to_encode = {"sub": user.username}
    if expires_delta:
        expire = datetime.now(tz=UTC) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now(tz=UTC) + timedelta(days=1)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        config.ACCESS_TOKEN_SECRET_KEY,
        algorithm=config.ACCESS_TOKEN_ALGORITHM,
    )


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token=token,
            key=config.ACCESS_TOKEN_SECRET_KEY,
            algorithms=config.ACCESS_TOKEN_ALGORITHM,
        )
    except jwt.JWTError:
        return None
    sub = payload.get("sub")
    if not isinstance(sub, str):
        return None
    return sub
