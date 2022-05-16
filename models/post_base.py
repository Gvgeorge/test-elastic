from pydantic import BaseModel
from datetime import datetime, timezone


class PostBase(BaseModel):
    created_datetime: datetime
    text: str

    class Config:
        orm_mode = True
