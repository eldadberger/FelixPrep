from typing import Optional

from pydantic import BaseModel, Field


class CreditBase(BaseModel):
    set_name: str = Field(..., alias="setName")
    author: Optional[str] = None
    source: Optional[str] = None
    license_name: Optional[str] = Field(None, alias="licenseName")
    license_source: Optional[str] = Field(None, alias="licenseSource")
    