from models.wine import Wine
from sqlalchemy.orm import Session

def create_wine(wine_data, db: Session):
    wine = Wine(**wine_data.dict())
    db.add(wine)
    db.commit()
    db.refresh(wine)
    return wine

def get_all_wines(db: Session):
    return db.query(Wine).all()

def get_wine_by_id(wine_id: int, db: Session):
    return db.query(Wine).filter(Wine.id == wine_id).first()

def update_wine(wine_id: int, wine_data, db: Session):
    wine = get_wine_by_id(wine_id, db)
    if not wine:
        return None

    for key, value in wine_data.dict().items():
        setattr(wine, key, value)

    db.commit()
    db.refresh(wine)
    return wine

def delete_wine(wine_id: int, db: Session):
    wine = get_wine_by_id(wine_id, db)
    if not wine:
        return None

    db.delete(wine)
    db.commit()
    return wine
