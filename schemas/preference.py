from pydantic import BaseModel, ConfigDict
from utils.validators.cpf import CPF

class PreferenceSchema(BaseModel):
    user_id: int
    wine_id: int

class PreferenceOutSchema(PreferenceSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
