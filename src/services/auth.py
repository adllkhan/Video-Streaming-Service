from core.exceptions import HTTPInvalidCredentials
from models import User
from repositories import UserRepository
from schemas.auth import CredentialsInSchema, TokenOutSchema
from utils.auth import create_access_token, verify_password


class AuthService:
    def __init__(self, repository: UserRepository = None):
        self.repository = repository

    async def authenticate(self, credentials: CredentialsInSchema) -> User | None:
        user = await self.repository.get_user_by_username(username=credentials.username)
        if not user or not verify_password(
            plain=credentials.password, hashed=user.password
        ):
            return None
        return user

    async def login(self, credentials: CredentialsInSchema) -> TokenOutSchema:
        user = await self.authenticate(credentials=credentials)
        if not user:
            raise HTTPInvalidCredentials(username=credentials.username)
        token = create_access_token(user=user)
        return TokenOutSchema(access_token=token)
