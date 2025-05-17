from typing import List

from pydantic import BaseModel, Field


class ConnectionResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    icons: List[dict]