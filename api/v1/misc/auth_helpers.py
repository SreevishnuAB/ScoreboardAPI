import logging
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from starlette.requests import Request
from fastapi.security.utils import get_authorization_scheme_param

import jwt
from jwt import PyJWTError
from api.v1.cookie import OAuth2PasswordBearerCookie
from config import Config

oauth2 = OAuth2PasswordBearerCookie(tokenUrl="api/v1/login")
logger = logging.getLogger()

def create_access_token(*, user: dict, expires_delta: timedelta = None):

    to_encode = user.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


def read_jwt(token: str = Depends(oauth2)):
    logger.info(token)
    unauth_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        user: str = payload.get("sub")
        logger.info(f"read {user}")
        if user is None:
            raise unauth_exception

    except PyJWTError:
        raise unauth_exception

    return user


def get_access_token(user: str):
    logger.info(f"get {user}")
    token_expiry = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user={"sub": user}, 
        expires_delta=token_expiry
    )
    return access_token