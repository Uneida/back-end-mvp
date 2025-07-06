from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from database.session import Base
from pydantic import BaseModel, Field
import re

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    preferences = relationship("Preference", back_populates="user")
    
    @validates('cpf')
    def validate_cpf(self, key, cpf):
        return re.sub(r'\D', '', cpf)


