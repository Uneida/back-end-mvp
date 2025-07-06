from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from database.session import Base, engine
from flask import g
from database.session import SessionLocal

from models.user import User
from models.wine import Wine
from models.preference import Preference

from routes.preference import register_preference_routes
from routes.user import register_user_routes
from routes.wine import register_wine_routes

info = Info(title="Wine Preference API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

Base.metadata.create_all(bind=engine)

@app.before_request
def before_request():
    g.db = SessionLocal()

@app.teardown_request
def teardown_request(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
@app.get("/")
def root():
    return {"message": "Welcome to the Wine Preference API"}

register_preference_routes(app)
register_user_routes(app)
register_wine_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
