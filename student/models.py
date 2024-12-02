from sqlalchemy import Column,Integer,String,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Address(Base):
    __tablename__ = "address"
    
    id = Column(Integer,primary_key=True,index=True)
    city = Column(String)
    country = Column(String)
    
    students = relationship("Student", back_populates="address", cascade="all, delete-orphan", single_parent=True)

class Student(Base):
    __tablename__ = "student"
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    age = Column(Integer)
    address_id = Column(Integer,ForeignKey('address.id',ondelete="CASCADE"))

    address = relationship("Address", back_populates="students")
    
