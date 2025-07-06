from models.preference import Preference
from sqlalchemy.orm import Session

def create_preference(preference_data, db: Session):
    """Create a new preference for a user."""
    preference = Preference(**preference_data.dict())  # Usando o mesmo padrão que o create_wine
    db.add(preference)
    db.commit()
    db.refresh(preference)
    return preference

def get_preferences_by_user(user_id: int, db: Session):
    """Get all preferences for a specific user."""
    return db.query(Preference).filter(Preference.user_id == user_id).all()

def update_preference(preference_id: int,user_id: int, user_cpf: str, wine_id: int, db: Session):
    """Update an existing preference by ID."""
    preference = db.query(Preference).filter(Preference.id == preference_id).first()
    if not preference:
        return None
    preference.user_id = user_id
    preference.user_cpf = user_cpf
    preference.wine_id = wine_id
    db.commit()
    db.refresh(preference)
    return preference

def delete_preference(preference_id: int, db: Session):
    """Delete a preference by ID."""
    preference = db.query(Preference).filter(Preference.id == preference_id).first()
    if not preference:
        return None
    db.delete(preference)
    db.commit()
    return preference

def get_all_preferences(db):
    return db.query(Preference).all()
