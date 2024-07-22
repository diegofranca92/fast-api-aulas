from database import Base
from sqlalchemy import Column, Integer, String

class ItemModel(Base):
  __tablename__ = 'items'

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  name = Column(String, index=True)
  description = Column(String, index=True)
  
