from typing import Optional
from pydantic import BaseModel


class IconUpdate(BaseModel):
    name: Optional[str] = None
    score: Optional[float] = None
