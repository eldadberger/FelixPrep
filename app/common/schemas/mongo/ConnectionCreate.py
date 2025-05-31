from pydantic import BaseModel


class ConnectionCreate(BaseModel):
    name: str
