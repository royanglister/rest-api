from db import Base
from sqlalchemy import String, Integer, Column

MAX_LENGTH = 255

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(MAX_LENGTH), nullable=False, unique=True)
    email = Column(String(MAX_LENGTH), nullable=False, unique=True)

    def __repr__(self):
        return f"<ID: {self.id}, Name: {self.name}, Email: {self.email}>"
