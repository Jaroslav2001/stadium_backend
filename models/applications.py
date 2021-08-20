from typing import Optional
from datetime import datetime
from odmantic import Model, Reference

from enums.status import Status


class Applications(Model):
    full_name: str
    datetime: datetime
    organization: str
    goal: str
    full_name_applications: str
    passport: str
    auto: Optional[str]
    note: str

    status: Status = Status.checkDepartmentHead
