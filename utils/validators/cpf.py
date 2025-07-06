import re
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

def is_valid_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calc_digit(digs):
        s = sum(int(d) * i for d, i in zip(digs, range(len(digs) + 1, 1, -1)))
        rest = 11 - s % 11
        return '0' if rest >= 10 else str(rest)

    dig1 = calc_digit(cpf[:9])
    dig2 = calc_digit(cpf[:9] + dig1)
    return cpf[-2:] == dig1 + dig2

class CPF(str):
    """
    Custom CPF type compatible with Pydantic v2 and OpenAPI schema generation.
    """

    @classmethod
    def validate(cls, v: str) -> str:
        if not isinstance(v, str):
            raise TypeError('string required')

        if not is_valid_cpf(v):
            raise ValueError('invalid CPF')

        return cls(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {
            "type": "string",
            "format": "cpf",
            "examples": ["12345678909"],
            "description": "Valid CPF number"
        }
