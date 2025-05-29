from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.handlers.exceptions_handler import exceptions_handler
from app.api.router import api_router
from app.settings import settings
import nest_asyncio

nest_asyncio.apply()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    openapi_url="/openapi.json",
)

app.include_router(api_router, prefix="/api")

app.add_exception_handler(Exception, exceptions_handler)

# Sets all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Guards against HTTP Host Header attacks
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
