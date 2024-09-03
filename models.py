from datbase import Base
from sqlalchemy import Column,Integer,String,Boolean

class Todos(Base):
    __tablename__ = 'todo'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    desc = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean,default=False)
