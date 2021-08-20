from fastapi import Depends, HTTPException
from typing import List

from fastapi import APIRouter
from database import engine
from models.role_user import RoleUser
from shemas.user import User
from .user import fastapi_users
from enums.role import Role
from pydantic import UUID4

api = APIRouter(prefix='/role_user', tags=['role_user'])
collection = 'role_user'


@api.put(
    '',
    response_model=RoleUser,
    dependencies=[Depends(
        fastapi_users.current_user(
           active=True,
           superuser=True
        )
    )]
)
async def func(
    id: UUID4,
    role: Role,
):
    role_user = RoleUser(
        user_id=id,
        role=role
    )
    user = await fastapi_users.db.get(id=id)
    if role_user.role.value == Role.Administrator.value:
        user.is_superuser = True
    else:
        user.is_superuser = False
    await engine.save(role_user)
    return role_user


@api.get(
    '',
    response_model=List[RoleUser],
    dependencies=[Depends(
        fastapi_users.current_user(
           active=True,
           superuser=True
        )
    )]
)
async def func():
    return await engine.find(RoleUser)


@api.get(
    '/{id}',
    response_model=RoleUser,
    dependencies=[Depends(
        fastapi_users.current_user(
           active=True,
           superuser=True
        )
    )]
)
async def func(
    id: UUID4
):
    user = await engine.find_one(
        RoleUser,
        RoleUser.user_id == id
    )
    if user is None:
        raise HTTPException(404)
    return user


@api.delete(
    '/{id}',
    response_model=RoleUser,
    dependencies=[Depends(
        fastapi_users.current_user(
           active=True,
           superuser=True
        )
    )]
)
async def func(
    id: UUID4
):
    user = await engine.find_one(
        RoleUser,
        RoleUser.user_id == id
    )
    if user is None:
        raise HTTPException(404)
    await engine.delete(user)
    return user
