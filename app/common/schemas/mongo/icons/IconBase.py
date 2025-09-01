from pydantic import BaseModel


class IconBase(BaseModel):
    name: str
    svg: str
