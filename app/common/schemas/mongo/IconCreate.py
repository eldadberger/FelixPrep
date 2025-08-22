from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class IconCreate(BaseModel):
    name: str = Field(..., min_length=1)
    svg: str = Field(..., min_length=1)
    credit: Optional[str] = None

    def to_mongo(self):
        data = self.dict()
        if self.credit_id:
            data["credit"] = ObjectId(self.credit)
        return data
