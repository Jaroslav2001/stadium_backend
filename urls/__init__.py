from fastapi import APIRouter

from . import user
from . import todo_list
from . import role_user
# from . import organization
from . import applications

api = APIRouter(prefix='/api')

api.include_router(user.api)
api.include_router(todo_list.api)
api.include_router(role_user.api)
# api.include_router(organization.api)
api.include_router(applications.api)
