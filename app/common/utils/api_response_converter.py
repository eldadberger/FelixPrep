from fastapi import status
from app.common.schemas.api_response import ApiResponse


def handle_response(class_type):
    def handle_response_inner(response):
        if status.HTTP_200_OK <= response.status_code < status.HTTP_300_MULTIPLE_CHOICES:
            return ApiResponse(status_code=response.status_code, response=response, class_type=class_type,
                               exception=None)
        else:
            return ApiResponse(status_code=response.status_code, exception=response.text(), class_type=None,
                               response=response)

    return handle_response_inner
