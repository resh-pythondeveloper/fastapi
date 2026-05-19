from sqlalchemy import Column,Table,Integer,String,Float
from db2 import Base

class Item(Base):
    __tablename__="items"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50),unique=True,index=True,nullable=True)
    price=Column(Float,nullable=True)
    quantity=Column(Integer,default=0)
