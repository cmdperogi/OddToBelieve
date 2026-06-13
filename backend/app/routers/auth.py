from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from app.models.schemas import Token

router = APIRouter(prefix="/auth", tags=["auth"])

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(
        {"sub": subject, "exp": expire},
        settings.secret_key,
        algorithm=settings.algorithm,
    )


@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    is_valid_user = form_data.username == settings.admin_username
    is_valid_password = form_data.password == settings.admin_password
    if not (is_valid_user and is_valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = _create_access_token(form_data.username)
    return Token(access_token=token, token_type="bearer")
