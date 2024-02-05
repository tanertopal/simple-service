from pydantic import BaseModel
 
class User(BaseModel): 
    id: int
    email: str
    password: str
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel): 
    email: str
    password: str
    
    class Config:
        orm_mode = True
