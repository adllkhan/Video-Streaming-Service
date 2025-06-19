from pydantic import BaseModel


class CredentialsInSchema(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {"username": "john_doe", "password": "securepassword123"}
        }


class TokenOutSchema(BaseModel):
    access_token: str
    scheme: str = "Bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwi"
                "aWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                "scheme": "Bearer",
            }
        }
