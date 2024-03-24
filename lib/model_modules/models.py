from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base
# from lib.db.session import sesfrom 
from model_modules import Base
# from __init__ import Base

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    instructions = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="recipes")
    average_rating = Column(Float)

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    recipes = relationship("Recipe", back_populates="category")


