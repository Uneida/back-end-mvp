from pydantic import BaseModel, ConfigDict
from utils.validators.name import Name

class WineSchema(BaseModel):
    grape: str
    country: str
    style: str

class WineOutSchema(WineSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
