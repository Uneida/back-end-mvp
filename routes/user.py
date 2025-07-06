from flask_openapi3 import Tag, request
from schemas.user import UserSchema, UserOutSchema
from repositories.user import (
    create_user,
    get_user_by_cpf,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)
from flask import jsonify, request, g
from sqlalchemy.exc import IntegrityError
from utils.serializer import ListAll
from logger import logger
from schemas.error import ErrorSchema
from utils.responses import *
from pydantic import BaseModel, Field

user_tag = Tag(name="User", description="User management")

class UserPath(BaseModel):
    user_id: int = Field(..., description='user_id')
    
def register_user_routes(app):
    @app.post("/user", tags=[user_tag], responses={
        201: USER_CREATED,
        404: error_response(kind="not_found", description="No users found"),
        400: error_response(kind="bad_request", description="Invalid data"),
    })
    def post_user_route(body: UserSchema):
        """Create a new user"""
        try:
            data = request.get_json()
            user_data = UserSchema(**data)
            user = create_user(user_data, g.db)
            logger.info(f"User created successfully: {user_data.cpf}")
            return UserOutSchema.model_validate(user).model_dump(), 201
        except IntegrityError:
            logger.warning(f"User already exists with CPF: {data.get('cpf')}")
            return jsonify({"message": "User already exists"}), 409
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return jsonify({"message": "Invalid user data", "error": str(e)}), 400

    @app.get("/users", tags=[user_tag], responses={
        201: USER_LIST,
        400: error_response(kind="not_found", description="No users found"),
    })
    def list_users_route():
        """List all users"""
        users = get_all_users(g.db)
        if not users:
            logger.warning("No users found in database.")
            return jsonify({"message": "No users found"}), 404
        logger.info(f"Fetched {len(users)} users from database.")
        return ListAll(users, UserOutSchema), 200

    # @app.get("/user/<string:cpf>", tags=[user_tag], responses={
    #     200: {"description": "User found", "content": {"application/json": {"example": {"cpf": "12345678901", "name": "John", "last_name": "Doe"}}}},
    #     404: {"description": "User not found", "content": {"application/json": {"example": {"message": "User not found"}}}},
    # })
    # def get_user_by_cpf_route():
    #     try:
    #         cpf = request.view_args['cpf']
    #         user = get_user_by_cpf(cpf, g.db)
    #         if not user:
    #             logger.warning(f"User not found with CPF: {cpf}")
    #             return jsonify({"message": "User not found"}), 404
    #         logger.info(f"User found: {cpf}")
    #         return UserOutSchema.model_validate(user).model_dump(), 200
    #     except Exception as e:
    #         logger.error(f"Error fetching user by CPF {cpf}: {str(e)}")
    #         return jsonify({"message": "Error fetching user", "error": str(e)}), 500

    @app.get("/user/<int:user_id>", tags=[user_tag], responses={
       201: response_schema(UserOutSchema, "Users retrieved"),
       404: error_response(kind="not_found", description="No users found"),
    })
    def get_user_by_id_route(path: UserPath):
        """Get a user by id"""
        try:
            user_id = request.view_args['user_id']
            user = get_user_by_id(user_id, g.db)
            if not user:
                logger.warning(f"User not found with CPF: {user_id}")
                return jsonify({"message": "User not found"}), 404
            logger.info(f"User found: {user_id}")
            return UserOutSchema.model_validate(user).model_dump(), 200
        except Exception as e:
            logger.error(f"Error fetching user by CPF {user_id}: {str(e)}")
            return jsonify({"message": "Error fetching user", "error": str(e)}), 500
        
    @app.put("/user/<int:user_id>", tags=[user_tag], responses={
        201: response_schema(UserOutSchema, "User updated successfully"),
        404: error_response(kind="not_found", description="No users found"),
        400: error_response(kind="bad_request", description="Invalid data"),
    })
    def put_user_route(path: UserPath, body: UserSchema):
        """Update a user by id"""
        try:
            user_id = request.view_args['user_id']
            data = request.get_json()
            user_data = UserSchema(**data)
            updated = update_user(user_id, user_data, g.db)
            if not updated:
                logger.warning(f"User not found for update with ID: {user_id}")
                return {"message": "User not found"}, 404
            logger.info(f"User updated successfully: {user_id}")
            return UserOutSchema.model_validate(updated).model_dump(), 200
        except Exception as e:
            logger.error(f"Error updating user ID {user_id}: {str(e)}")
            return {"message": "Failed to update user", "error": str(e)}, 400

    @app.delete("/user/<int:user_id>", tags=[user_tag], responses={
        201: response_schema(UserOutSchema, "User deleted successfully"),
        404: error_response(kind="not_found", description="No users found"),
    })
    def delete_user_route(path: UserPath):
        """Delete a user by id"""
        try:
            user_id = request.view_args['user_id']
            deleted = delete_user(user_id, g.db)
            if not deleted:
                logger.warning(f"User not found for deletion with ID: {user_id}")
                return {"message": "User not found"}, 404
            logger.info(f"User deleted successfully: {user_id}")
            return {"message": f"User {user_id} deleted"}, 200
        except Exception as e:
            logger.error(f"Error deleting user ID {user_id}: {str(e)}")
            return {"message": "Failed to delete user", "error": str(e)}, 500
