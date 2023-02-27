from typing import Optional
from pydantic import BaseModel


class SchemaSearch(BaseModel):
    link: str
    title: Optional[str] = None
    author: Optional[str] = None
    keywords: Optional[str] = None

    class Config:
        orm_mode = True
