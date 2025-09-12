from typing import Optional, List

from bson import ObjectId
from pydantic import Field
from app.common.schemas.mongo.credits.CreditReponse import CreditResponse
from app.common.schemas.mongo.helpers.PyObjectId import PyObjectId
from app.common.schemas.mongo.icons.IconBase import IconBase
from app.common.schemas.mongo.tags.TagResponse import TagResponse
from app.common.utils.replace_id_helper import replace_id_recursive


class IconExpandedResponse(IconBase):
    id: PyObjectId = Field(alias="_id")
    credit: Optional[CreditResponse] = None
    tags: List[TagResponse] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)

        return replace_id_recursive(data)
