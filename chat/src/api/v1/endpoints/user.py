from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from chat.src.core.security import get_current_user, create_access_token
from chat.src.schemas.user import TokenSchema, UserCreateSchema, UserResponseSchema
from chat.src.services.user_service import UserService
from chat.src.core.config import settings
from chat.src.services.dependencies import get_user_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponseSchema)
async def register(
    user_data: UserCreateSchema, service: UserService = Depends(get_user_service)
):
    return await service.register_user(user_data)


@router.post("/login", response_model=TokenSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponseSchema)
async def get_me(current_user: UserResponseSchema = Depends(get_current_user)):
    return current_user
