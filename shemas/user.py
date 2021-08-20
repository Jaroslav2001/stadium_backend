from fastapi_users import models


class User(models.BaseUser):
    full_name: str


class UserCreate(models.BaseUserCreate):
    full_name: str


class UserUpdate(User, models.BaseUserUpdate):
    full_name: str


class UserDB(User, models.BaseUserDB):
    full_name: str
