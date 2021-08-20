from enum import Enum


class Role(str, Enum):
    Director = 'Директор'
    DepartmentHead = 'Начальник Отдела'
    SecurityService = 'Служба Безопасности'
    Security = 'Охрана'
    Administrator = 'Администратор'
