import re
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

class Name(str):
    """
    Custom Name type: must contain only letters and spaces, length 2–100.
    """

    @classmethod
    def validate(cls, v: str) -> str:
        if not isinstance(v, str):
            raise TypeError("string required")

        if len(v) < 2 or len(v) > 100:
            raise ValueError("Name must be between 2 and 100 characters")

        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', v):
            raise ValueError("Name must only contain letters and spaces")

        return cls(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {
            "type": "string",
            "format": "name",
            "examples": ["Alice", "João da Silva"],
            "description": "Name with letters and spaces only (2–100 chars)"
        }
