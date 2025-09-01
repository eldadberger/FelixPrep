from typing import Optional
from pydantic import BaseModel, Field


class CreditUpdate(BaseModel):
    set_name: Optional[str] = Field(None, alias="setName")
    author: Optional[str] = None
    source: Optional[str] = None
    license_name: Optional[str] = Field(None, alias="licenseName")
    license_source: Optional[str] = Field(None, alias="licenseSource")
