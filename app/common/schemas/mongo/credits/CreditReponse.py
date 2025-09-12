from bson import ObjectId
from pydantic import Field
from app.common.schemas.mongo.credits.CreditBase import CreditBase
from app.common.schemas.mongo.helpers.PyObjectId import PyObjectId
from app.common.utils.replace_id_helper import replace_id_recursive


class CreditResponse(CreditBase):
    id: PyObjectId = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)

        return replace_id_recursive(data)
