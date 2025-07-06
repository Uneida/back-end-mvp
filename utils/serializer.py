from typing import TypeVar, Type, List
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

def ListAll(data: List, schema: Type[T]):
    """
    Retorna uma lista de dicionários Pydantic (já com .model_dump()),
    pronta para ser retornada diretamente de uma rota Flask.
    """
    return [schema.model_validate(obj).model_dump() for obj in data]
