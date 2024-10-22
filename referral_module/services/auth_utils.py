from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from typing import Annotated, Union
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from authlib.integrations.starlette_client import OAuth
from http import HTTPStatus
import jwt
import os
from dotenv import load_dotenv

from referral_module.models.repository import UsersRepository, CodesRepository

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    refresh_token_url=None,
    api_base_url="https://www.googleapis.com",
    redirect_uri=GOOGLE_REDIRECT_URI,
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)


def get_hash_password(plain_password):
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str):
    user_service = UsersRepository()
    user = await user_service.get_by_email(email=email)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def auth_user_func(email: str, password: str):
    user = await authenticate_user(email=email, password=password)
    if not user:
        raise Exception("Incorrect username or password")
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"email": user["email"], "id": user["id"]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def register_user_func(email: str, password: str = None, ref_code: str = None):
    user_service = UsersRepository()
    code_service = CodesRepository()
    user = await user_service.get_by_email(email=email)
    if user:
        raise Exception("User with this email already exist")

    hashed_password = None
    if password:
        hashed_password = get_hash_password(plain_password=password)
    referr_id = None
    if ref_code:
        code = await code_service.get_code_by_ref_code(code=ref_code)
        if (
            not code
            or datetime.strptime(code["expired_date"], "%Y-%m-%d %H:%M:%S.%f")
            < datetime.now()
        ):
            raise Exception("Invalid referral code")
        referr_id = code["user_id"]

    new_user = await user_service.create_user(
        email=email, hashed_password=hashed_password, referr_id=referr_id
    )

    return new_user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        id: int = payload.get("id")
        if not email or not id:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user_service = UsersRepository()
    user = await user_service.get_by_id(id=id)
    if user is None:
        raise credentials_exception
    return user


async def auth_google_callback(request, ref_code: str = None):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    user_service = UsersRepository()
    user = await user_service.get_by_email(user_info["email"])
    if not user:
        user = await register_user_func(email=user_info["email"], ref_code=ref_code)
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"email": user["email"], "id": user["id"]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
