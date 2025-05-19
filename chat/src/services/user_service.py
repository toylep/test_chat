from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from chat.src.db.models import User
from chat.src.schemas.user import TokenSchema, UserCreateSchema
from chat.src.repositories.user_repo import UserRepository
from chat.src.core.config import settings
from chat.src.services.base import BaseService
from chat.src.schemas.user import UserCreateSchema, UserResponseSchema, UserLoginSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)


class UserService(BaseService[UserCreateSchema, UserRepository]):
    response_schema = UserResponseSchema

    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.auth = AuthService()

    async def register_user(self, user_data: UserCreateSchema) -> User:
        existing_user = await self.repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = self.auth._get_password_hash(user_data.password)
        new_user = await self.repo.add(
            {
                "name": user_data.name,
                "email": user_data.email,
                "hashed_password": hashed_password,
            }
        )
        return new_user

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.repo.get_by_email(email)
        if not user or not self.auth._verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        return user

    async def get_all_by_id(self, ids: list[int]):
        users = await self.repo.get_with_filters({"id": list(ids)})
        return [self.response_schema.model_validate(user.__dict__) for user in users]

    async def get_by_email(self, email: str):
        user = await self.repo.get_by_email(email)
        return self.response_schema.model_validate(user.__dict__)
