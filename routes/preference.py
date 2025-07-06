from flask_openapi3 import Tag
from schemas.preference import PreferenceSchema, PreferenceOutSchema
from repositories.preference import (
    create_preference, get_preferences_by_user,
    update_preference, delete_preference, get_all_preferences
)
from flask import request, g
from sqlalchemy.exc import IntegrityError
from utils.serializer import ListAll
from logger import logger
from schemas.error import ErrorSchema
from utils.responses import *
from pydantic import BaseModel, Field

preference_tag = Tag(name="Preference", description="User's wine preferences")

class PreferencePath(BaseModel):
    preference_id: int = Field(..., description='preference_id')
    
def register_preference_routes(app):
    # POST: Create a preference
    @app.post("/preference", tags=[preference_tag], responses={
        201: PREFERENCE_CREATED,
        409: error_response(kind="conflict",description="Preference already exists"),
        400: error_response(kind="bad_request",description="Invalid preference data")
    })
    def post_preference_route(body: PreferenceSchema):
        """Create a new preference"""
        try:
            data = request.get_json()
            preference_data = PreferenceSchema(**data)
            preference = create_preference(preference_data, g.db)
            logger.info(f"Preference created: user_cpf={preference_data.user_id}, wine_id={preference_data.wine_id}")
            return PreferenceOutSchema.model_validate(preference).model_dump(), 201
        except IntegrityError:
            logger.warning(f"Duplicate preference: {data}")
            return {"message": "Preference already exists"}, 409
        except Exception as e:
            logger.error(f"Error creating preference: {str(e)}")
            return {"message": "Invalid preference data", "error": str(e)}, 400

    # # GET: List all preferences for a user
    # @app.get("/preferences/<int:user_id>", tags=[preference_tag], responses={
    #     200: PREFERENCE_LIST,
    #     404: error_response(kind="not_found", description="No preferences found"),
    # })
    # def get_preference_route():
    #     """List all for a user preference by user id"""
    #     try:
    #         user_id = request.view_args["user_id"]
    #         preferences = get_preferences_by_user(user_id, g.db)
    #         if not preferences:
    #             logger.warning(f"No preferences found for user: {user_id}")
    #             return {"message": "No preferences found"}, 404
    #         logger.info(f"Preferences fetched for user: {user_id}")
    #         return ListAll(preferences, PreferenceOutSchema), 200
    #     except Exception as e:
    #         logger.error(f"Error fetching preferences for user {user_id}: {str(e)}")
    #         return {"message": "Error fetching preferences", "error": str(e)}, 500

        # GET: List all preferences (independent of user)
    @app.get("/preferences", tags=[preference_tag], responses={
        200: PREFERENCE_LIST,
        404: error_response(kind="not_found", description="No preferences found")
    })
    def list_all_preferences():
        """Get all preferences in the system"""
        try:
            preferences = get_all_preferences(g.db)
            if not preferences:
                logger.warning("No preferences found in the system.")
                return {"message": "No preferences found"}, 404
            logger.info("Fetched all preferences from the system.")
            return ListAll(preferences, PreferenceOutSchema), 200
        except Exception as e:
            logger.error(f"Error fetching all preferences: {str(e)}")
            return {"message": "Failed to fetch preferences", "error": str(e)}, 500

    # PUT: Update a preference
    @app.put("/preference/<int:preference_id>", tags=[preference_tag], responses={
        200: response_schema(PreferenceOutSchema, "Preference updated successfully"),
        404: error_response(kind="not_found", description="No preferences found"),
        400: error_response(kind="bad_request", description="Invalid data"),
    })
    def put_preference_route(path: PreferencePath, body: PreferenceSchema):
        """Update a preference by id"""
        try:
            preference_id = request.view_args["preference_id"]
            data = request.get_json()
            preference_data = PreferenceSchema(**data)
            updated = update_preference(preference_id, preference_data.user_id, preference_data.user_cpf, preference_data.wine_id, g.db)
            if not updated:
                logger.warning(f"Preference not found for update: ID={preference_id}")
                return {"message": "Preference not found"}, 404
            logger.info(f"Preference updated: ID={preference_id}")
            return PreferenceOutSchema.model_validate(updated).model_dump(), 200
        except Exception as e:
            logger.error(f"Error updating preference ID {preference_id}: {str(e)}")
            return {"message": "Failed to update preference", "error": str(e)}, 400

    # DELETE: Remove a preference
    @app.delete("/preference/<int:preference_id>", tags=[preference_tag], responses={
        200: response_schema(PreferenceOutSchema, "Preference deleted successfully"),
        404: error_response(kind="not_found", description="No preferences found"),
    })
    def delete_preference_route(path: PreferencePath, body: PreferenceSchema):
        """Remove a preference by id"""
        try:
            preference_id = request.view_args["preference_id"]
            deleted = delete_preference(preference_id, g.db)
            if not deleted:
                logger.warning(f"Preference not found for deletion: ID={preference_id}")
                return {"message": "Preference not found"}, 404
            logger.info(f"Preference deleted: ID={preference_id}")
            return {"message": f"Preference {preference_id} deleted"}, 200
        except Exception as e:
            logger.error(f"Error deleting preference ID {preference_id}: {str(e)}")
            return {"message": "Failed to delete preference", "error": str(e)}, 500
