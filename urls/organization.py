from fastapi import Depends, HTTPException
from typing import List

from fastapi import APIRouter
from database import engine

from models.organization import Organization
from .user import fastapi_users
from bson import ObjectId


api = APIRouter(prefix='/organization', tags=['organization'])
collection = 'organization'


@api.put(
    '',
    response_model=Organization,
    dependencies=[Depends(
        fastapi_users.current_user(
           active=True,
           superuser=True
        )
    )]
)
async def func(
    name: str
):
    organization = Organization(
        name=name
    )
    print(organization)
    await engine.save(organization)
    return organization


@api.get(
    '',
    response_model=List[Organization],
    dependencies=[Depends(
        fastapi_users.current_user(
           active=True,
           superuser=True
        )
    )]
)
async def func():
    return await engine.find(Organization)


@api.delete(
    '/{id}',
    response_model=Organization,
    dependencies=[Depends(
        fastapi_users.current_user(
           active=True,
           superuser=True
        )
    )]
)
async def func(
    id: str
):
    name = await engine.find_one(
        Organization,
        Organization.id == ObjectId(id)
    )
    if name is None:
        raise HTTPException(404)
    await engine.delete(name)
    return name
