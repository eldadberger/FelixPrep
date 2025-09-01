from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field

from app.common.schemas.mongo.credits.CreditBase import CreditBase
from app.common.schemas.mongo.helpers.PyObjectId import PyObjectId
from app.common.schemas.mongo.tags.TagBase import TagBase


class IconRead(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    svg: str
    credit: Optional[CreditBase] = None
    tags: List[TagBase] = []

    class Config:
        validate_by_name = True
        json_encoders = {ObjectId: str}
