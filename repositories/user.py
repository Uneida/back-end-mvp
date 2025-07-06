from models.user import User
from sqlalchemy.orm import Session

def create_user(user_data, db: Session):
    """Create a new user in the database."""
    user = User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    """Get all users."""
    return db.query(User).all()

def get_user_by_id(user_id: int, db: Session):
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_cpf(cpf: str, db: Session):
    """Get a user by CPF."""
    return db.query(User).filter(User.cpf == cpf).first()

def update_user(user_id: int, user_data, db: Session):
    """Update an existing user by ID."""
    user = get_user_by_id(user_id, db)
    if not user:
        return None

    for key, value in user_data.dict().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id: int, db: Session):
    """Delete a user by ID."""
    user = get_user_by_id(user_id, db)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return user
