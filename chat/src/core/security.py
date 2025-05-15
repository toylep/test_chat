from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from chat.src.core.config import settings
from chat.src.db.dependencies import get_db
from chat.src.db.models import User

from chat.src.services.dependencies import get_user_service
from chat.src.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.jwt.SECRET_KEY, algorithms=[settings.jwt.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await service.get_by_email(email)

    if result is None:
        raise credentials_exception
    return result


def create_access_token(data: dict[any, any]) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.jwt.SECRET_KEY, algorithm=settings.jwt.ALGORITHM
    )
