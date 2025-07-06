# schemas/error.py

from pydantic import BaseModel

class ErrorSchema(BaseModel):
    message: str
    details: str | None = None

    class Config:
        json_schema_extra = {
            "examples": {
                "bad_request": {
                    "message": "Invalid preference data",
                    "details": "Field 'wine_id' is required"
                },
                "conflict": {
                    "message": "Preference already exists",
                    "details": None
                },
                "not_found": {
                    "message": "Resource not found",
                    "details": None
                }
            }
        }
