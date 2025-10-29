from typing import Dict, Any
from pydantic import BaseModel, Field


class MutationWeight(BaseModel):
    background_decoration: float = Field(0, alias="backgroundDecoration")
    symmetric_x: float = Field(0, alias="symmetricX")
    symmetric_y: float = Field(0, alias="symmetricY")
    colors: dict
