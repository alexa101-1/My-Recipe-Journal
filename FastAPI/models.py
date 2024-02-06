from sqlalchemy import Column, Integer, String, ARRAY
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(500))
    prep_time = Column(String(20))
    cook_time = Column(String(20))
    total_time = Column(String(20))
    level = Column(String(20))
    rating = Column(Integer)
    people = Column(Integer)
