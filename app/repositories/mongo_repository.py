from fastapi import HTTPException
from typing import Optional
from bson import ObjectId
from pymongo import ASCENDING

from app.common.schemas.mongo.credits.CreditCreate import CreditCreate
from app.common.schemas.mongo.deprecated.Credit import Credit
from starlette import status
from app.common.schemas.mongo.icons.IconCreate import IconCreate
from app.common.schemas.mongo.icons.IconExapndedResponse import IconExpandedResponse
from app.common.schemas.mongo.tags.TagCreate import TagCreate
from app.common.schemas.mongo.tags.TagResponse import TagResponse


class MongoRepository:
    def __init__(self, client):
        self.client = client
        self.db = self.client["felix"]
        self.icons = self.db["icons"]
        self.tags = self.db["tags"]
        self.credits = self.db["credits"]
        self._ensure_indexes()

    def _ensure_indexes(self):
        self.icons.create_index("name", unique=True)
        self.icons.create_index("svg", unique=True)
        self.tags.create_index("name", unique=True)
        self.credits.create_index(
            [("set_name", ASCENDING), ("author", ASCENDING)],
            unique=True
        )

    def get_all_icons_expanded(self, name: Optional[str] = None):
        pipeline = []

        if name is not None:
            pipeline.append({
                "$match": {"name": {"$regex": name, "$options": "i"}}
            })

        pipeline = pipeline + [
            {
                "$lookup": {
                    "from": "credits",
                    "localField": "credit",
                    "foreignField": "_id",
                    "as": "credit"
                }
            },
            {
                "$lookup": {
                    "from": "tags",
                    "localField": "tags",
                    "foreignField": "_id",
                    "as": "tags"
                }
            },
            {
                "$addFields": {
                    "credit": {"$arrayElemAt": ["$credit", 0]}
                }
            }
        ]

        icons = list(self.icons.aggregate(pipeline))
        return [IconExpandedResponse(**icon).model_dump(by_alias=True) for icon in icons]

    def get_icon_by_id(self, icon_id: str):
        pipeline = [
            {
                "$match": {"_id": ObjectId(icon_id)}
            },
            {
                "$lookup": {
                    "from": "credits",
                    "localField": "credit",
                    "foreignField": "_id",
                    "as": "credit"
                }
            },
            {
                "$lookup": {
                    "from": "tags",
                    "localField": "tags",
                    "foreignField": "_id",
                    "as": "tags"
                }
            },
            {
                "$addFields": {
                    "credit": {"$arrayElemAt": ["$credit", 0]}
                }
            }
        ]

        icon = list(self.icons.aggregate(pipeline))
        if icon:
            return IconExpandedResponse(**icon[0]).model_dump(by_alias=True)
        raise HTTPException(status_code=404, detail="Icon not found")

    def create_icon(self, icon: IconCreate) -> str:
        result = self.icons.insert_one(icon.to_mongo())
        return str(result.inserted_id)

    def update_icon_by_id(
            self,
            icon_id: str,
            name: Optional[str] = None,
            svg: Optional[str] = None,
            credit_id: Optional[ObjectId] = None
    ):
        update_fields = {}
        unset_fields = {}

        if name is not None:
            update_fields["name"] = name
        if svg is not None:
            update_fields["svg"] = svg
        if credit_id is not None:
            update_fields["credit"] = credit_id
        elif credit_id is None:
            unset_fields["credit"] = ""

        if not update_fields and not unset_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field (name, svg or credit_id) must be provided for update."
            )

        update_query = {}
        if update_fields:
            update_query["$set"] = update_fields
        if unset_fields:
            update_query["$unset"] = unset_fields

        result = self.icons.find_one_and_update(
            {"_id": ObjectId(icon_id)},
            update_query,
            return_document=True
        )

        pipeline = [
            {"$match": {"_id": result["_id"]}},
            {
                "$lookup": {
                    "from": "credits",
                    "localField": "credit",
                    "foreignField": "_id",
                    "as": "credit"
                }
            },
            {
                "$lookup": {
                    "from": "tags",
                    "localField": "tags",
                    "foreignField": "_id",
                    "as": "tags"
                }
            },
            {"$addFields": {"credit": {"$arrayElemAt": ["$credit", 0]}}},
        ]

        expanded = self.icons.aggregate(pipeline).to_list(length=1)
        return IconExpandedResponse(**expanded[0]).model_dump(by_alias=True)

    def delete_icon(self, icon_id):
        icon_id = ObjectId(icon_id)

        self.icons.delete_one({"_id": icon_id})

    def get_all_tags(self):
        tags = list(self.tags.find({}))
        return [TagResponse(**tag).dict() for tag in tags]

    def get_single_tag(self, tag_id):
        tag = self.tags.find_one({"_id": ObjectId(tag_id)})
        return TagResponse(**tag).dict()

    def get_tag_icons(self, tag_id: str):
        pipeline = [
            {"$match": {"tags": {"$in": [ObjectId(tag_id)]}}},
            {
                "$lookup": {
                    "from": "credits",
                    "localField": "credit",
                    "foreignField": "_id",
                    "as": "credit"
                }
            },
            {
                "$lookup": {
                    "from": "tags",
                    "localField": "tags",
                    "foreignField": "_id",
                    "as": "tags"
                }
            },
            {
                "$addFields": {
                    "credit": {"$arrayElemAt": ["$credit", 0]}
                }
            }
        ]

        icons = list(self.icons.aggregate(pipeline))
        return [IconExpandedResponse(**icon).dict() for icon in icons]

    def create_tag(self, tag: TagCreate) -> str:
        result = self.tags.insert_one(tag.dict())
        return str(result.inserted_id)

    def update_tag(self, tag_id: str, tag: TagCreate):
        result = self.tags.update_one(
            {"_id": ObjectId(tag_id)},
            {"$set": {"name": tag.name}}
        )

        if not result.matched_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="tag not found."
            )

    def delete_tag(self, tag_id):
        self.tags.delete_one({"_id": ObjectId(tag_id)})

    def add_tag_to_icon(self, icon_id: str, tag_id: str):
        icon = self.icons.find_one({"_id": ObjectId(icon_id)})
        if not icon:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Icon not found")

        tag = self.tags.find_one({"_id": ObjectId(tag_id)})
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found")

        self.icons.update_one(
            {"_id": ObjectId(icon_id)},
            {"$addToSet": {"tags": ObjectId(tag_id)}}
        )

    def remove_tag_from_icon(self, icon_id: str, tag_id: str):
        self.icons.update_one(
            {"_id": ObjectId(icon_id)},
            {"$pull": {"tags": ObjectId(tag_id)}}
        )

    def get_all_credits(self):
        res = list(self.credits.find({}))
        return [
            {
                "id": str(c["_id"]),
                "setName": c.get("setName"),
                "author": c.get("author"),
                "source": c.get("source"),
                "licenseName": c.get("licenseName"),
                "licenseSource": c.get("licenseSource"),
            }
            for c in res
        ]

    def insert_credit(self, credit: CreditCreate):
        doc = credit.model_dump(by_alias=True)
        result = self.credits.insert_one(doc)
        return {"id": str(result.inserted_id)}

    def update_credit_by_id(self, credit_id: str, update_data: dict):
        result = self.credits.update_one(
            {"_id": ObjectId(credit_id)},
            {"$set": update_data}
        )
        return result.modified_count

    def connect_credit_to_icon(self, icon_id: str, credit_id: str):
        result = self.icons.update_one(
            {"_id": ObjectId(icon_id)},
            {"$set": {"credit": ObjectId(credit_id)}}
        )
        return result.modified_count

    def disconnect_credit_from_icon(self, icon_id: str):
        result = self.icons.update_one(
            {"_id": ObjectId(icon_id)},
            {"$unset": {"credit": ""}}
        )
        return result.modified_count

    def delete_credit(self, credit_id: str):
        credit = self.credits.find_one({"_id": ObjectId(credit_id)})
        if not credit:
            raise HTTPException(status_code=404, detail="Credit not found")

        self.icons.update_many(
            {"credit": ObjectId(credit_id)},
            {"$unset": {"credit": ""}}  # removes the field
        )

        self.credits.delete_one({"_id": ObjectId(credit_id)})
