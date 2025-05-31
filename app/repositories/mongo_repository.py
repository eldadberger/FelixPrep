from fastapi import HTTPException
from typing import Optional
from bson import ObjectId
from app.common.schemas.mongo.ConnectionCreate import ConnectionCreate
from app.common.schemas.mongo.IconCreate import IconCreate
from starlette import status


class MongoRepository:
    def __init__(self, client):
        self.client = client
        self.db = self.client["felix"]
        self.icons = self.db["icons"]
        self.connections = self.db["connections"]
        self._ensure_indexes()

    def _ensure_indexes(self):
        self.icons.create_index("name", unique=True)
        self.icons.create_index("svg", unique=True)
        self.connections.create_index("name", unique=True)

    def get_icon(self, icon_id: Optional[str], name: Optional[str], with_connections: bool = False):
        query = {}
        if icon_id:
            query["_id"] = ObjectId(icon_id)
        elif name:
            query["name"] = name
        else:
            icons = list(self.icons.find())
            icon_list = []

            for icon in icons:
                icon_data = {
                    "id": str(icon["_id"]),
                    "name": icon["name"],
                    "svg": icon["svg"]
                }

                if with_connections:
                    connections = self.connections.find(
                        {"icons.id": icon["_id"]},
                        {"name": 1}
                    )
                    icon_data["connections"] = [
                        {"id": str(c["_id"]), "name": c["name"]} for c in connections
                    ]

                icon_list.append(icon_data)

            return icon_list

        icon = self.icons.find_one(query)
        if not icon:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        icon_data = {
            "id": str(icon["_id"]),
            "name": icon["name"],
            "svg": icon["svg"]
        }

        if with_connections:
            connections = self.connections.find(
                {"icons.id": icon["_id"]},
                {"name": 1}
            )
            icon_data["connections"] = [
                {"id": str(c["_id"]), "name": c["name"]} for c in connections
            ]

        return icon_data

    def create_icon(self, icon: IconCreate) -> str:
        result = self.icons.insert_one(icon.dict())
        return str(result.inserted_id)

    def update_icon_by_id(self, icon_id: str, name: Optional[str] = None, svg: Optional[str] = None):
        icon_obj_id = ObjectId(icon_id)

        update_fields = {}
        if name is not None:
            update_fields["name"] = name
        if svg is not None:
            update_fields["svg"] = svg

        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field (name or svg) must be provided for update."
            )

        result = self.icons.update_one(
            {"_id": icon_obj_id},
            {"$set": update_fields}
        )

        if not result.matched_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Icon not found."
            )

        updated_icon = self.icons.find_one({"_id": icon_obj_id})
        if updated_icon is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Updated icon could not be retrieved."
            )

        return {
            "id": str(updated_icon["_id"]),
            "name": updated_icon["name"],
            "svg": updated_icon["svg"]
        }

    def delete_icon_and_remove_references(self, icon_id):
        icon_id = ObjectId(icon_id)

        self.icons.delete_one({"_id": icon_id})
        self.connections.update_many(
            {"icons.id": icon_id},
            {"$pull": {"icons": {"id": icon_id}}}
        )

    def get_all_connections_with_icons(self):
        all_conns = self.connections.find()
        result = []

        for conn in all_conns:
            icon_ids = [icon["id"] for icon in conn.get("icons", [])]
            icon_map = {
                str(icon["_id"]): icon
                for icon in self.icons.find({"_id": {"$in": icon_ids}})
            }

            expanded = []
            for icon_ref in conn.get("icons", []):
                icon_id = str(icon_ref["id"])
                icon_data = icon_map.get(icon_id)
                if icon_data:
                    expanded.append({
                        "id": icon_id,
                        "name": icon_data["name"],
                        "svg": icon_data["svg"],
                        "score": icon_ref["score"]
                    })

            result.append({
                "id": str(conn["_id"]),
                "name": conn["name"],
                "icons": expanded
            })

        return result

    def get_connection_with_icons(self, connection_id: str):
        query = {"_id": ObjectId(connection_id)}
        conn = self.connections.find_one(query)
        if not conn:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found")

        icon_map = {
            str(icon["_id"]): icon
            for icon in self.icons.find({"_id": {"$in": [icon["id"] for icon in conn.get("icons", [])]}})
        }

        expanded = []
        for icon_ref in conn.get("icons", []):
            icon_id = str(icon_ref["id"])
            icon_data = icon_map.get(icon_id)
            if icon_data:
                expanded.append({
                    "id": icon_id,
                    "name": icon_data["name"],
                    "svg": icon_data["svg"],
                    "score": icon_ref["score"]
                })

        return {"id": str(conn["_id"]), "name": conn["name"], "icons": expanded}

    def create_connection(self, conn: ConnectionCreate) -> str:
        result = self.connections.insert_one({"name": conn.name, "icons": []})
        return str(result.inserted_id)

    def update_connection(self, connection_id: str, conn: ConnectionCreate):
        connection_id = ObjectId(connection_id)
        result = self.connections.update_one(
            {"_id": connection_id},
            {"$set": {"name": conn.name}}
        )

        if not result.matched_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Connection not found."
            )

    def delete_connection(self, connection_id):
        self.connections.delete_one({"_id": ObjectId(connection_id)})

    def add_icon_to_connection(self, icon_id: str, connection_id: str, score: float):
        icon = self.icons.find_one({"_id": ObjectId(icon_id)})
        if not icon:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Icon not found")

        conn = self.connections.find_one({"_id": ObjectId(connection_id)})
        if not conn:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found")

        # Ensure connection exists and icon is not already in it
        result = self.connections.update_one(
            {
                "_id": ObjectId(connection_id),
                "icons.id": {"$ne": ObjectId(icon_id)}  # Only add if not already present
            },
            {
                "$push": {"icons": {"id": ObjectId(icon_id), "score": score}}
            }
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Icon already in connection"
            )

    def remove_icon_from_connection(self, connection_id: str, icon_id: str):
        result = self.connections.update_one(
            {"_id": ObjectId(connection_id)},
            {"$pull": {"icons": {"id": ObjectId(icon_id)}}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Icon not found in connection")

    def update_icon_score(self, connection_id: str, icon_id: str, score: float):
        result = self.connections.update_one(
            {
                "_id": ObjectId(connection_id),
                "icons.id": ObjectId(icon_id)
            },
            {
                "$set": {"icons.$.score": score}
            }
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def get_connections_by_icon(self, icon_id: str):
        icon_obj_id = ObjectId(icon_id)
        connections = self.connections.find(
            {"icons.id": icon_obj_id},
            {"name": 1}  # Only return name field plus _id by default
        )
        return [{"id": str(conn["_id"]), "name": conn["name"]} for conn in connections]

