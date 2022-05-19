from pydantic import BaseModel


class RubricBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
