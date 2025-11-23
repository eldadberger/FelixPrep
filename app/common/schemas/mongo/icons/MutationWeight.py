from typing import Dict, Any, List
from pydantic import BaseModel, Field

from app.common.schemas.mongo.icons.ColorItem import ColorItem


class MutationWeight(BaseModel):
    background_decoration: float = Field(0, alias="backgroundDecoration")
    symmetric_x: float = Field(0, alias="symmetricX")
    symmetric_y: float = Field(0, alias="symmetricY")
    colors: List[ColorItem]
