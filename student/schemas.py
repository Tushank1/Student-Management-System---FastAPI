from pydantic import BaseModel
from typing import Optional,List

class Address(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None

class Details(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address : Optional[Address] = None
    
class ShowDetail(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Address 
    
    class Config:
        from_attributes = True
        
class StudentListResponse(BaseModel):
    data: List[Details]
    