from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base
# from lib.db.session import sesfrom 
from model_modules import Base
# from __init__ import Base

class Instruction(Base):
    
    __tablename__ = 'instructions'
    id = Column(Integer, primary_key=True)
    step = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    recipe = relationship("Recipe", back_populates="instructions")