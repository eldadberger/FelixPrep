from typing import TypeVar, Optional, Generic
from requests import Response
from pydantic.tools import parse_obj_as
from fastapi import HTTPException, status

T = TypeVar('T')


class ApiResponse(Generic[T]):
    status_code: int
    response: Response
    exception: Optional[str]
    class_type: Optional[T]

    def __init__(self, status_code, exception, response, class_type):
        self.status_code = status_code
        self.exception = exception
        self.response = response
        self.class_type = class_type

    def is_success_status_code(self):
        return status.HTTP_200_OK <= self.status_code < status.HTTP_300_MULTIPLE_CHOICES

    def get_data(self) -> T:
        try:
            if self.class_type == str:
                return self.response.text
            body = self.response.json()
            return parse_obj_as(self.class_type, body)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error parsing answer from {self.response.url}: {str(e)}")
