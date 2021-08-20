from fastapi import status, Depends, HTTPException
from typing import List

from bson import ObjectId
from fastapi import APIRouter
from database import engine
from shemas import User
from models.todo_list import TodoList, UpdateTodoList
from .user import fastapi_users


api = APIRouter(prefix='/todo_list', tags=['todo_list'])
collection = 'todo_list'


@api.put('', response_model=TodoList)
async def func(
    todo_list: TodoList,
    user: User = Depends(fastapi_users.current_user(active=True))
):
    todo_list.user_id = user.id
    print(user)
    print(todo_list)
    await engine.save(todo_list)
    return todo_list.json()


@api.get('', response_model=List[TodoList])
async def func(
    user: User = Depends(fastapi_users.current_user(active=True))
):
    return await engine.find(TodoList, TodoList.user_id == user.id)


@api.get('/count', response_model=int)
async def func(
    user: User = Depends(fastapi_users.current_user(active=True))
):
    return await engine.count(TodoList, user.id == TodoList.user_id)


@api.get('/{id}', response_model=TodoList)
async def func(
    id: str,
    user: User = Depends(fastapi_users.current_user(active=True))
):
    todo = await engine.find_one(
        TodoList,
        TodoList.id == ObjectId(id),
        user.id == TodoList.user_id
    )
    if todo is None:
        raise HTTPException(404)
    return todo


@api.delete('/{id}', response_model=TodoList)
async def func(
    id: str,
    user: User = Depends(fastapi_users.current_user(active=True))
):
    todo = await engine.find_one(
        TodoList,
        TodoList.id == ObjectId(id),
        user.id == TodoList.user_id
    )
    if todo is None:
        raise HTTPException(404)
    await engine.delete(todo)
    return todo


@api.patch('/{id}', response_model=TodoList)
async def func(
    id: str,
    patch: UpdateTodoList,
    user: User = Depends(fastapi_users.current_user(active=True))
):
    todo = await engine.find_one(TodoList, TodoList.id == ObjectId(id))
    if todo is None:
        raise HTTPException(404)
    elif todo.user_id != user.id:
        raise HTTPException(401)

    patch_dict = patch.dict(exclude_unset=True)
    for name, value in patch_dict.items():
        setattr(todo, name, value)
    await engine.save(todo)
    return todo
