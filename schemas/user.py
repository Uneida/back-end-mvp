from pydantic import BaseModel, ConfigDict
from utils.validators.cpf import CPF
from utils.validators.name import Name

class UserSchema(BaseModel):
    cpf: CPF
    first_name: str
    last_name: str

class UserOutSchema(UserSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
