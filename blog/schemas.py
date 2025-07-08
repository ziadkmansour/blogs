from typing import Optional
from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str
    
    class Config:
        orm_mode = True


class Blogs(BaseModel):
    blogs: List[Blog]
    
    class Config:
        orm_mode = True
        
class User(BaseModel):
    username: str
    email: str
    password: str
    
    class Config:
        orm_mode = True