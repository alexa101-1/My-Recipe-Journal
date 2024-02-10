from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
import database
from sqlalchemy.orm import mapped_column
from typing import List
from database import Base
from typing import Optional


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))


recipe_ingredients_assoc = Table('recipe_ingredient', Base.metadata,
                                 Column('recipe_id', Integer, ForeignKey('recipes.id')),
                                 Column('ingredient_id', Integer, ForeignKey('ingredients.id')))

# class BaseModel(Base):
#     __abstract__ = True
#     __allow_unmapped__ = True


class Recipe(Base):
    __tablename__ = "recipes"

    # id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(500))
    # ingredients = Column(String(2000))
    prep_time = Column(String(20))
    cook_time = Column(String(20))
    total_time = Column(String(20))
    level = Column(String(20))
    rating = Column(Integer)
    people = Column(Integer)
    id = Column(Integer, primary_key=True)
    ingredients = relationship("Ingredients", secondary=recipe_ingredients_assoc)


class Ingredients(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)



