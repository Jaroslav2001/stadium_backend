from fastapi import APIRouter, Request
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import JWTAuthentication
from fastapi_users import FastAPIUsers

from setting import setting
from database import db
from shemas import UserDB, User, UserCreate, UserUpdate


collection = db.users
user_db = MongoDBUserDatabase(UserDB, collection)


def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


jwt_authentication = JWTAuthentication(
    secret=setting.SECRET, lifetime_seconds=3600, tokenUrl="api/auth/jwt/login"
)

api = APIRouter()
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
api.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"]
)
api.include_router(
    fastapi_users.get_register_router(on_after_register),
    prefix="/auth",
    tags=["auth"]
)
api.include_router(
    fastapi_users.get_reset_password_router(
        setting.SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_verify_router(
        setting.SECRET, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"]
)
