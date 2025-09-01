from bson import ObjectId
from pydantic import Field
from app.common.schemas.mongo.credits.CreditBase import CreditBase
from app.common.schemas.mongo.helpers.PyObjectId import PyObjectId


class CreditResponse(CreditBase):
    id: PyObjectId = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
