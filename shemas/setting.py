from pydantic import BaseModel


class Setting(BaseModel):
    DATABASE_URL: str
    DATABASE_DB: str
    SECRET: str
    SERVER: dict
    DATABASE: dict
    CORS: dict
