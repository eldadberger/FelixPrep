from typing import Optional

from bson import ObjectId
from pydantic import BaseModel


class Credit(BaseModel):
    id: Optional[str] = None
    set_name: Optional[str] = None
    author: Optional[str] = None
    source: Optional[str] = None
    license_name: Optional[str] = None
    license_url: Optional[str] = None

    @classmethod
    def from_mongo(cls, doc):
        if not doc:
            return None
        return cls(
            id=str(doc["_id"]),
            set_name=doc["set_name"],
            author=doc["author"],
            source=doc["source"],
            license_name=doc["license_name"],
            license_url=doc["license_url"],
        )