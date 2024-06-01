from pydantic import BaseModel, Field
from datetime import datetime


class AppInfo(BaseModel):
    application: str = Field()
    version: str = Field()
    started_at: datetime = Field()
