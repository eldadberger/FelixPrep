from fastapi import APIRouter

from app.api.endpoints import felix
from app.api.endpoints.external import svg_router

api_router = APIRouter()
api_router.include_router(svg_router.router, prefix="/external", tags=["external"])
api_router.include_router(felix.router, tags=["api"])
