from odmantic import Model, Field
from pydantic import UUID4

from enums.role import Role


class RoleUser(Model):
    user_id: UUID4 = Field(primary_field=True)
    role: Role


class UpdateRoleUser(Model):
    role: Role
