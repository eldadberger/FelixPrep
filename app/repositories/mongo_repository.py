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
            icons = self.icons.find()
            return [
                {
                    "id": str(icon["_id"]),
                    "name": icon["name"],
                    "svg": icon["svg"]
                }
                for icon in icons
            ]

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

    def get_connection_with_icons(self, connection_id: Optional[str] = None, name: Optional[str] = None):
        query = {"_id": ObjectId(connection_id)} if connection_id else {"name": name}
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

        return {"_id": str(conn["_id"]), "name": conn["name"], "icons": expanded}

    def create_connection(self, conn: ConnectionCreate) -> str:
        result = self.connections.insert_one({"name": conn.name, "icons": []})
        return str(result.inserted_id)

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


    def delete_icon_and_remove_references(self, icon_id: str):
        icon_id = ObjectId(icon_id)

        # Delete the icon from the icon collection
        icon_result = self.icons.delete_one({"_id": icon_id})

        # Remove the icon from all connections
        connection_result = self.connections.update_many(
            {"icons.id": icon_id},
            {"$pull": {"icons": {"id": icon_id}}}
        )
