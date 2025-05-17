from uplink import Consumer, post, Body, json, get, Query, response_handler

from app.common.schemas.api_response import ApiResponse
from app.common.utils.api_response_converter import handle_response


@json
class SvgRepository(Consumer):
    def __init__(self, base_url, client):
        super(SvgRepository, self).__init__(base_url=base_url, client=client)

    def update_headers(self, headers):
        self.session.headers.update(headers)

    @response_handler(handle_response(dict))
    @get("/_next/data/BDi4Qmi5UPf9aqlnfRTY9/vectors/{json_term}")
    def search_svgs(self, json_term: str, term: Query(type=list[str])) -> ApiResponse[dict]: pass

    @response_handler(handle_response(str))
    @get("/show/{id}/{slug}.svg")
    def get_svg(self, id: str, slug: str) -> ApiResponse[str]: pass
