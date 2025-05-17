from pydantic import BaseModel


class SvgIcon(BaseModel):
    id: str
    slug: str
    title: str
