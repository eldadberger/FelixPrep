import requests
from typing import Generator
from fastapi import Depends
from pymongo import MongoClient

from app.repositories.mongo_repository import MongoRepository
from app.repositories.svg_repository import SvgRepository
from app.settings import settings


def get_requests_session() -> Generator[requests.Session, None, None]:
    session = requests.Session()
    try:
        yield session
    finally:
        session.close()


client = MongoClient(settings.MONGO_URL)


def get_mongo_repository():
    return MongoRepository(client=client)


def get_svg_repository(session=Depends(get_requests_session)):
    consumer = SvgRepository(base_url=settings.SVG_REPOSITORY_BASE_URL, client=session)
    return consumer
