from pydantic import BaseModel


class UsersOut(BaseModel):
    user_id: int
    username: str


class UserOut(UsersOut):
    first_name: str
    last_name: str


class UserIn(BaseModel):
    username: str
    first_name: str
    last_name: str
