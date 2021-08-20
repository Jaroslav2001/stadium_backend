from enum import Enum


class Status(str, Enum):
    checkDepartmentHead = 'checkDepartmentHead'
    checkDirector = 'checkDirector'
    checkSecurityService = 'checkSecurityService'
    checkSecurity = 'checkSecurity'
    successfully = 'successfully'
    refusal = 'refusal'
