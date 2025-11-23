from typing import Optional

from pydantic import BaseModel


class ColorItem(BaseModel):
    key: str
    weight: float
    required: Optional[bool] = None
