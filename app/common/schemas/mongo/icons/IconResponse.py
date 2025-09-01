from typing import Optional, List
from bson import ObjectId
from pydantic import Field
from app.common.schemas.mongo.helpers.PyObjectId import PyObjectId
from app.common.schemas.mongo.icons.IconBase import IconBase


class IconResponse(IconBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    credit: Optional[PyObjectId] = None
    tags: List[PyObjectId] = []

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
