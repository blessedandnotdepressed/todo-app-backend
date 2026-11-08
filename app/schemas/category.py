from pydantic import BaseModel, ConfigDict


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str

class CategoryUpdateOrCreate(BaseModel):
    name: str

