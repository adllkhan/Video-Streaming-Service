from pydantic import BaseModel, Field


class UserOutSchema(BaseModel):
    user_id: int = Field(alias="id")
    username: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": 6,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
            }
        }


class UserUpdateSchema(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "password": "securepassword123",
            }
        }


class UserInSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "password": "securepassword123",
            }
        }
