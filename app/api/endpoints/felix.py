from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, Query
from app.common.schemas.mongo.ConnectionCreate import ConnectionCreate
from app.common.schemas.mongo.ConnectionResponse import ConnectionResponse
from app.common.schemas.mongo.Credit import Credit
from app.common.schemas.mongo.IconScore import IconScore
from app.common.schemas.mongo.icons.IconCreate import IconCreate
from app.common.schemas.mongo.tags.TagCreate import TagCreate
from app.repositories.deps import get_mongo_repository
from app.repositories.mongo_repository import MongoRepository

router = APIRouter()


@router.get("/icons")
def get_icons(db: Annotated[MongoRepository, Depends(get_mongo_repository)],
              name: Optional[str] = Query(None)):
    return db.get_all_icons_expanded(name)


@router.get("/icons/{icon_id}")
def get_icon(icon_id: str, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    return db.get_icon_by_id(icon_id)


@router.post("/icons", response_model=dict)
def create_icon(icon: IconCreate, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    return {"id": db.create_icon(icon)}


@router.put("/icons/{icon_id}")
def update_icon(icon_id: str, icon: IconCreate, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    return db.update_icon_by_id(icon_id, icon.name, icon.svg, icon.credit)


@router.delete("/icons/{icon_id}")
def delete_icon(
        icon_id: str,
        db: Annotated[MongoRepository, Depends(get_mongo_repository)]
):
    db.delete_icon(icon_id)
    return {"removed": True}


@router.get("/tags")
def get_all_tags(db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    return db.get_all_tags()


@router.get("/tags/{tag_id}/icons")
def get_tag_icons(db: Annotated[MongoRepository, Depends(get_mongo_repository)], tag_id: str):
    return db.get_tag_icons(tag_id)


@router.post("/tags", response_model=dict)
def create_tag(conn: TagCreate, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    return {"id": db.create_tag(conn)}


@router.put("/tags/{tag_id}")
def update_connection(tag_id: str, tag: TagCreate,
                      db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    db.update_tag(tag_id, tag)


@router.delete("/tags/{tag_id}")
def delete_connection(tag_id: str, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    db.delete_tag(tag_id)


@router.patch("/icons/{icon_id}/tags/{tag_id}", response_model=dict)
def add_tag_to_icon(
        icon_id: str,
        tag_id: str,
        db: Annotated[MongoRepository, Depends(get_mongo_repository)]
):
    db.add_tag_to_icon(icon_id, tag_id)
    return {"added": True}


@router.delete("/icons/{icon_id}/tags/{tag_id}", response_model=dict)
def remove_tag_from_icon(
        icon_id: str,
        tag_id: str,
        db: Annotated[MongoRepository, Depends(get_mongo_repository)]
):
    db.remove_tag_from_icon(icon_id, tag_id)
    return {"removed": True}


@router.get("/credits")
def get_credits(db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    return db.get_all_credits()


@router.post("/credits")
def insert_credit(credit: Credit, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    return db.insert_credit(credit)


@router.patch("/credits/{credit_id}")
def update_credit_by_id(credit_id: str, update_data: Credit,
                        db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    db.update_credit_by_id(credit_id, update_data.dict())
    return {"updated": True}


@router.post("/icons/{icon_id}/credits/{credit_id}")
def connect_credit_to_icon(icon_id: str, credit_id: str, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    db.connect_credit_to_icon(icon_id, credit_id)
    return {"connected": True}


@router.delete("/icons/{icon_id}/credits")
def disconnect_credit_from_icon(icon_id: str, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    db.disconnect_credit_from_icon(icon_id)
    return {"disconnected": True}


@router.delete("/credits/{credit_id}")
def delete_credit(credit_id: str, db: Annotated[MongoRepository, Depends(get_mongo_repository)]):
    db.delete_credit(credit_id)
    return {"deleted": True}
