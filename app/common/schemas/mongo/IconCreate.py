from typing import Optional
from pydantic import BaseModel, Field


class IconCreate(BaseModel):
    name: str = Field(..., min_length=1)
    svg: str = Field(..., min_length=1)
