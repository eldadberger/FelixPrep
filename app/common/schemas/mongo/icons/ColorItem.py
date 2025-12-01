from typing import Optional

from pydantic import BaseModel, Field

from app.common.schemas.mongo.icons.ColorType import ColorType


class ColorItem(BaseModel):
    key: str
    weight: float
    required: Optional[bool] = None
    type: Optional[ColorType] = None
