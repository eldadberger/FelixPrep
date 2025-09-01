from bson import ObjectId
from pydantic import Field
from app.common.schemas.mongo.helpers.PyObjectId import PyObjectId
from app.common.schemas.mongo.tags.TagBase import TagBase


class TagResponse(TagBase):
    id: PyObjectId = Field(alias="_id")

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
