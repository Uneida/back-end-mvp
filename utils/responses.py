from schemas.error import ErrorSchema
from schemas.preference import PreferenceOutSchema
from schemas.user import UserOutSchema
from schemas.wine import WineOutSchema

def response_schema(schema, description: str):
    return {
        "description": description,
        "content": {"application/json": {"schema": schema.schema()}}
    }

def response_list_schema(schema, description: str):
    # Gera um schema OpenAPI para um array de itens do schema dado
    return {
        "description": description,
        "content": {
            "application/json": {
                "schema": {
                    "type": "array",
                    "items": schema.model_json_schema()
                }
            }
        }
    }
    
def error_response(kind: str, description: str):
    """
    kind: chave dentro de ErrorSchema.Config.json_schema_extra['examples']
    description: texto exibido no OpenAPI para esse status code
    """
    example = ErrorSchema.Config.json_schema_extra["examples"][kind]
    return {
        "description": description,
        "content": {
            "application/json": {
                "schema": ErrorSchema.model_json_schema(),
                "example": example
            }
        }
    }

# HTTP_400 = error_response("Invalid data")
# HTTP_404 = error_response("Resource not found")
# HTTP_409 = error_response("Resource already exists")

PREFERENCE_CREATED = response_schema(PreferenceOutSchema, "Preference created successfully")
USER_CREATED = response_schema(UserOutSchema, "User created successfully")
WINE_CREATED = response_schema(WineOutSchema, "Wine created successfully")
PREFERENCE_LIST    = response_list_schema(PreferenceOutSchema, "List of preferences")
USER_LIST          = response_list_schema(UserOutSchema,       "List of users")
WINE_LIST          = response_list_schema(WineOutSchema,       "List of wines")