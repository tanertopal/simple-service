from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()

class User(Base): 
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(50), nullable=False)
    password: str = Column(String(50), nullable=False)