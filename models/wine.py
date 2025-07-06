from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.session import Base

class Wine(Base):
    __tablename__ = "wines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    grape = Column(String, nullable=False) # Uva preferida
    country = Column(String, nullable=False)
    style = Column(String, nullable=False)

    preferences = relationship("Preference", back_populates="wine")
