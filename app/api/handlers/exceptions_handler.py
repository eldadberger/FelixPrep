from fastapi import Request
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.responses import JSONResponse


def exceptions_handler(request: Request, exc: Exception):
    if isinstance(exc, DuplicateKeyError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "duplicate error", "violation": exc.details["keyValue"]},
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content="An unexpected error occurred!",
    )
