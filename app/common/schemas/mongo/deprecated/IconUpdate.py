from typing import Optional
from pydantic import BaseModel


class IconUpdate(BaseModel):
    name: Optional[str] = None
    svg: Optional[str] = None
    credit: Optional[str] = None
