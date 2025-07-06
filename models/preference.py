from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    user_cpf = Column(Integer, ForeignKey("users.id"))
    wine_id = Column(Integer, ForeignKey("wines.id"))

    user = relationship("User", back_populates="preferences")
    wine = relationship("Wine", back_populates="preferences")
