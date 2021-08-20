from fastapi import status, Depends, HTTPException
from typing import List

from bson import ObjectId
from fastapi import APIRouter
from database import engine
from enums import Role
from enums.status import Status
from shemas import User
from models.todo_list import TodoList, UpdateTodoList
from models.applications import Applications
from models.role_user import RoleUser
from .user import fastapi_users
from pydantic import UUID4

api = APIRouter(prefix='/applications', tags=['applications'])
collection = 'applications'


@api.get(
    '/full',
    response_model=List[Applications],
    dependencies=[
        Depends(
            fastapi_users.current_user(
                active=True
            )
        )
    ]
)
async def func():
    return await engine.find(Applications)


@api.get(
    '/expectation',
    response_model=List[Applications]
)
async def func(
    user: User = Depends(
        fastapi_users.current_user(
            active=True
        )
    )
):
    role_user = await engine.find_one(
        RoleUser, RoleUser.user_id == user.id
    )
    if role_user is None:
        HTTPException(401)

    if role_user.role.value == Role.Administrator:
        return await engine.find(Applications)
    elif role_user.role.value == Role.DepartmentHead:
        return await engine.find(Applications, Applications.status == Status.checkDepartmentHead)
    elif role_user.role.value == Role.Director:
        return await engine.find(Applications, Applications.status == Status.checkDirector)
    elif role_user.role.value == Role.SecurityService:
        return await engine.find(Applications, Applications.status == Status.checkSecurityService)
    elif role_user.role.value == Role.Security:
        return await engine.find(Applications, Applications.status == Status.checkSecurity)


@api.post(
    '',
    response_model=Applications,
)
async def func(
        applications: Applications
):
    data = await engine.find_one(Applications, Applications.id == applications.id)
    print(data)
    if not(data is None):
        raise HTTPException(400)
    applications.status = Status.checkDepartmentHead.value
    await engine.save(applications)
    return applications


@api.patch(
    '/{id}',
    response_model=Applications
)
async def func(
        id: str,
        check: bool,
        user: User = Depends(
            fastapi_users.current_user(
                active=True
            )
        )
):
    role_user = await engine.find_one(
        RoleUser, RoleUser.user_id == user.id
    )
    applications = await engine.find_one(
        Applications, Applications.id == ObjectId(id)
    )
    if applications is None:
        HTTPException(404)
    if role_user is None:
        HTTPException(401)

    if not check:
        applications.status = Status.refusal.value
    elif applications.status == Status.checkDepartmentHead.value \
            and role_user.role.value == Role.DepartmentHead.value:
        applications.status = Status.checkDirector.value

    elif applications.status == Status.checkDirector.value \
            and role_user.role.value == Role.Director.value:
        applications.status = Status.checkSecurityService.value

    elif applications.status == Status.checkSecurityService.value \
            and role_user.role.value == Role.SecurityService.value:
        applications.status = Status.checkSecurity.value

    elif applications.status == Status.checkSecurity.value \
            and role_user.role.value == Role.Security.value:
        applications.status = Status.successfully.value
    else:
        HTTPException(401)
    await engine.save(applications)
    return applications


@api.get(
    '/{id}',
    response_model=Applications
)
async def func(
    id: str
):
    return await engine.find_one(Applications, Applications.id == ObjectId(id))


@api.get(
    '',
    response_model=List[Applications]
)
async def func(
    full_name: str
):
    return await engine.find(
        Applications,
        Applications.full_name == full_name
    )
