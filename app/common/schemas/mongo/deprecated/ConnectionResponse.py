from typing import List

from pydantic import BaseModel


class ConnectionResponse(BaseModel):
    id: str
    name: str
    icons: List[dict]
