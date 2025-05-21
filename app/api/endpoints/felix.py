from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from app.common.schemas.mongo.ConnectionCreate import ConnectionCreate
from app.common.schemas.mongo.ConnectionResponse import ConnectionResponse
from app.common.schemas.mongo.IconCreate import IconCreate
from app.common.schemas.mongo.IconUpdate import IconUpdate
from app.repositories.deps import get_mongo_repository
from app.repositories.mongo_repository import MongoRepository

router = APIRouter()


@router.get("/icons")
def get_icons(db: Annotated[MongoRepository, Depends(get_mongo_repository)],
              icon_id: Optional[str] = None,
              name: Optional[str] = None,
              ):
    result = db.get_icon(icon_id, name)
    if isinstance(result, list):
        return [{**icon, "_id": str(icon["_id"])} for icon in result]
    else:
        return {**result, "_id": str(result["_id"])}


@router.post("/icons", response_model=dict)
def create_icon(icon: IconCreate, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    return {"id": db.create_icon(icon)}


@router.get("/connections")
def get_all_connections(db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    return db.get_all_connections_with_icons()


@router.get("/connections/detail", response_model=ConnectionResponse)
def get_connection_detail(db: Annotated[MongoRepository, Depends(get_mongo_repository)],
                          connection_id: Optional[str] = None,
                          name: Optional[str] = None,
                          ):
    if not connection_id and not name:
        raise HTTPException(status_code=400, detail="You must have connection identifier (id/name)")
    return db.get_connection_with_icons(connection_id, name)


@router.post("/connections", response_model=dict)
def create_connection(conn: ConnectionCreate, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    return {"id": db.create_connection(conn)}


@router.post("/connections/{connection_name}/icons/{icon_id}", response_model=dict)
def add_icon_to_connection(
        connection_id: str,
        icon_id: str,
        score: float,
        db: Annotated[MongoRepository, Depends(get_mongo_repository)]
):
    db.add_icon_to_connection(icon_id, connection_id, score)
    return {"added": True}


@router.delete("/connections/{connection_id}/icons/{icon_id}", response_model=dict)
def remove_icon(
    connection_id: str,
    icon_id: str,
    db: Annotated[MongoRepository, Depends(get_mongo_repository)]
):
    db.remove_icon_from_connection(connection_id, icon_id)
    return {"removed": True}


@router.put("/connections/{connection_id}/icon/{icon_id}/score", response_model=dict)
def update_icon_score(
    connection_id: str,
    icon_id: str,
    score: float,
    db: Annotated[MongoRepository, Depends(get_mongo_repository)]
):
    db.update_icon_score(connection_id, icon_id, score)
    return {"updated": True}


@router.get("/icons/{icon_id}/connections", response_model=list[dict])
def get_connections_for_icon(icon_id: str, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    return db.get_connections_by_icon(icon_id)
