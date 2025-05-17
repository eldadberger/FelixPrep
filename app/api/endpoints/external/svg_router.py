from typing import Annotated
from fastapi import APIRouter, Query, Depends
from app.services.deps import get_svg_service
from app.services.svg_service import SvgService
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/search")
def search_svgs(term: Annotated[str, Query(max_length=25)],
                page: Annotated[int, Query()] = 1,
                service: SvgService = Depends(get_svg_service)) -> dict:
    return service.search_svgs(term=term, page=page)


@router.get("/{id}/{slug}.svg", response_class=PlainTextResponse)
def get_svg(id: str, slug: str,
            service: SvgService = Depends(get_svg_service)):
    return service.get_svg(id=id, slug=slug)
