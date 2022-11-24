from typing import List, Optional

from pydantic import BaseModel, validator


class Marketplace(BaseModel):
    id: str
    name: str
    description: str
    icon: Optional[str]

    @validator('icon')
    def set_icon(cls, icon):
        return icon or '/static/images/mkp.svg'


class Settings(BaseModel):
    marketplaces: List[Marketplace] = []
