from flask_openapi3 import Tag
from schemas.wine import WineSchema, WineOutSchema
from repositories.wine import (
    create_wine, get_all_wines, get_wine_by_id,
    update_wine, delete_wine
)
from flask import request, g
from sqlalchemy.exc import IntegrityError
from utils.serializer import ListAll
from logger import logger
from schemas.error import ErrorSchema
from utils.responses import *
from pydantic import BaseModel, Field

wine_tag = Tag(name="Wine", description="Wine catalog")

class WinePath(BaseModel):
    wine_id: int = Field(..., description='wine_id')
    
def register_wine_routes(app):
    # POST: Create a wine
    @app.post("/wine", tags=[wine_tag], responses={
        201: WINE_CREATED,
        409: error_response(kind="conflict",description="User already exists"),
        400: error_response(kind="bad_request",description="Invalid data")
    })
    def post_wine_route(body: WineSchema):
        """Add a new wine to the catalog"""
        try:
            data = request.get_json()
            wine_data = WineSchema(**data)
            wine = create_wine(wine_data, g.db)
            logger.info(f"Wine created successfully: {wine_data.grape}")
            return WineOutSchema.model_validate(wine).model_dump(), 201
        except IntegrityError:
            logger.error(f"IntegrityError while creating wine: {data}")
            return {"message": "Wine already exists"}, 409
        except Exception as e:
            logger.error(f"Error while creating wine: {str(e)}")
            return {"message": "Invalid wine data", "error": str(e)}, 400

    # GET: List all wines
    @app.get("/wines", tags=[wine_tag], responses={
        200: WINE_LIST,
        404: error_response(kind="not_found", description="No wines found"),
    })
    def get_wines_route():
        """Get the list of all wines in the catalog"""
        wines = get_all_wines(g.db)
        if not wines:
            logger.warning("No wines found in the catalog.")
            return {"message": "No wines found"}, 404
        return ListAll(wines, WineOutSchema), 200

    # GET: Get a wine by ID
    @app.get("/wine/<int:wine_id>", tags=[wine_tag], responses={
       201: response_schema(UserOutSchema, "Wine retrieved"),
       404: error_response(kind="not_found", description="No users found"),
    })
    def get_wine_route(path: WinePath):
        """Get a wine by its ID"""
        try:
            wine_id = request.view_args['wine_id']
            wine = get_wine_by_id(wine_id, g.db)
            if not wine:
                return {"message": "Wine not found"}, 404
            return WineOutSchema.model_validate(wine).model_dump(), 200
        except Exception as e:
            logger.error(f"Error fetching wine with ID {wine_id}: {str(e)}")
            return {"message": "Error fetching wine", "error": str(e)}, 500

    # PUT: Update wine
    @app.put("/wine/<int:wine_id>", tags=[wine_tag], responses={
        201: response_schema(WineOutSchema, "Wine updated successfully"),
        404: error_response(kind="not_found", description="No wines found"),
        400: error_response(kind="bad_request", description="Invalid data"),
    })
    def put_wine_route(path: WinePath, body: WineSchema):
        """Update a wine by its ID"""
        try:
            wine_id = request.view_args['wine_id']
            data = request.get_json()
            wine_data = WineSchema(**data)
            updated = update_wine(wine_id, wine_data, g.db)
            if not updated:
                return {"message": "Wine not found"}, 404
            return WineOutSchema.model_validate(updated).model_dump(), 200
        except Exception as e:
            logger.error(f"Error updating wine with ID {wine_id}: {str(e)}")
            return {"message": "Failed to update wine", "error": str(e)}, 400
        
    # DELETE: Remove wine
    @app.delete("/wine/<int:wine_id>", tags=[wine_tag], responses={
        200: response_schema(WineOutSchema, "Wine deleted successfully"),
        404: error_response(kind="not_found", description="No preferences found"),
    })
    def delete_wine_route(path: WinePath):
        """Delete a wine by its ID"""
        try:
            wine_id = request.view_args['wine_id']
            deleted = delete_wine(wine_id, g.db)
            if not deleted:
                return {"message": "Wine not found"}, 404
            return {"message": f"Wine {wine_id} deleted"}, 200
        except Exception as e:
            logger.error(f"Error deleting wine with ID {wine_id}: {str(e)}")
            return {"message": "Failed to delete wine", "error": str(e)}, 500
