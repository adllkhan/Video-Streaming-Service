from pydantic import BaseModel


class UsersOut(BaseModel):
    user_id: int
    username: str


class UserOut(UsersOut):
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserIn(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
