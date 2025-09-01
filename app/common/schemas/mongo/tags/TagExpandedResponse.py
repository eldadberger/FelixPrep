from typing import List
from app.common.schemas.mongo.icons.IconExapndedResponse import IconExpandedResponse
from app.common.schemas.mongo.tags.TagResponse import TagResponse


class TagExpandedResponse(TagResponse):
    icons: List[IconExpandedResponse] = []
