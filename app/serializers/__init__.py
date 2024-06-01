from pydantic import BaseModel, Field
from typing import Optional


class QueryPagination(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1)


class Pageinfo(BaseModel):
    page: int = Field()
    page_size: int = Field()
    next_page: Optional[str] = Field(default=None)
    previous_page: Optional[str] = Field(default=None)
