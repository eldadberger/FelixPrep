from fastapi import Depends
from app.repositories.deps import get_svg_repository
from app.services.svg_service import SvgService


def get_svg_service(svg_repository=Depends(get_svg_repository)):
    return SvgService(svg_repository=svg_repository)
