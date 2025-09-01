from typing import Optional, List

from bson import ObjectId
from pydantic import field_validator

from app.common.schemas.mongo.helpers.PyObjectId import PyObjectId
from app.common.schemas.mongo.icons.IconBase import IconBase


class IconCreate(IconBase):
    credit: Optional[PyObjectId] = None

    def to_mongo(self):
        data = self.dict()
        if self.credit:
            data["credit"] = ObjectId(self.credit)
        return data
