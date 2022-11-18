from typing import List, Optional

from pydantic import BaseModel


class Marketplace(BaseModel):
    id: str
    name: str
    description: str
    icon: Optional[str] = (
        'https://unpkg.com/@cloudblueconnect'
        '/material-svg@latest/icons/google/language/baseline.svg'
    )


class Settings(BaseModel):
    marketplaces: List[Marketplace] = []
