from fastapi import HTTPException
from starlette import status

from app.repositories.svg_repository import SvgRepository


class SvgService:
    def __init__(self, svg_repository: SvgRepository):
        self.__svg_repository = svg_repository

    def search_svgs(self, term: str, page: int):
        self.__svg_repository.update_headers({'x-nextjs-data': '1'})

        if page == 1:
            res = self.__svg_repository.search_svgs(f"{term}.json", [term])
        else:
            res = self.__svg_repository.search_svgs(f"{page}.json", [term, page])

        if res.is_success_status_code():
            return res.get_data()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.exception)

    def get_svg(self, id: str, slug: str):
        res = self.__svg_repository.get_svg(id, slug)

        if res.is_success_status_code():
            return res.get_data()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.exception)
