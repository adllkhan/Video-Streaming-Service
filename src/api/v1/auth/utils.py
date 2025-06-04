from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from src.api.v1.auth.constants import ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=30)
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta  # noqa: DTZ003
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
