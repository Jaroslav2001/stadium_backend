from typing import Optional
from odmantic import Model
from pydantic import UUID4


class TodoList(Model):
    text: str
    user_id: Optional[UUID4]


class UpdateTodoList(Model):
    text: Optional[str]
