import logging
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.sql import select, join
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder


# TODO create db user model
from db import database
from models.database.user import users
from models.request.auth import User, UserPassword, Hash
from .auth_helpers import get_access_token, read_jwt
from starlette.responses import Response


from models.response.auth import LoginResponse



logger = logging.getLogger()
router = APIRouter()
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), response: Response = Response()):
    
    # raise exception for NX_USER
    query = select([users]).where(users.c.id == form_data.username.lower())
    result = await database.fetch_one(query=query)
    if result == None:
        raise HTTPException(status_code=404, detail="User Not Found")
    #response = None
    if crypt_context.verify(form_data.password, result["password"]):
        token = get_access_token(result["id"])
        token = jsonable_encoder(token)
        response.set_cookie(
            "Authorization",
            value=f"Bearer {token}",
            secure=True,
            samesite="None",
            httponly=True,
            max_age=1800,
            expires=1800
        )
        return {"authenticated": True, "id": result["id"]}

    else:
        raise HTTPException(status_code=401, detail="Incorrect Username or Password")


@router.patch("/{user_id}/password")
async def update_password(user_id: str, pwd_data: UserPassword, jwt_user: str =  Depends(read_jwt)):

    user_id = user_id.lower()

    if jwt_user.lower() != user_id:
        raise HTTPException(
        status_code=403,
        detail="Unauthorised content",
        )

    query = select([users.c.password]).where(users.c.id == user_id)
    result = await database.fetch_one(query=query)
    
    if result == None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if crypt_context.verify(pwd_data.cur_pwd.get_secret_value(), result["password"]):
        hashed_pwd = crypt_context.hash(pwd_data.new_pwd.get_secret_value())
        stmt = users.update(None).\
                where(users.c.id == user_id).\
                values(password=hashed_pwd)
        await database.execute(stmt)
    else:
        raise HTTPException(
            status_code=401,
            detail="User could not be authenticated"
        )
    return  "Password changed"




@router.get("/logout")
def logout():
    response = Response()
    response.delete_cookie("Authorization")
    return "You have been logged out"


@router.post("/hash")
def generate_hash(hash_obj: Hash):
    hash = crypt_context.hash(str(hash_obj.password))
    return {"hash": hash}
