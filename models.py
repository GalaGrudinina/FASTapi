from sqlalchemy import Column,String,Text
from database import Base 

class Vessel(Base):
    __tablename__ = 'vessels'
    name=Column(String)
    id = Column(String)
    naccsCode= Column(String, primary_key=True, unique=True)
    date=Column(String)
    destination=Column(String)
    
    
    
    