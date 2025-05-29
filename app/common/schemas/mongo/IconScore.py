from typing import Optional

from pydantic import BaseModel


class IconScore(BaseModel):
    score: Optional[float] = None
