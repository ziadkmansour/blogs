from typing import List
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True

class Blog(BaseModel):
    title: str
    body: str

class UserMiniOut(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True

class BlogOut(BaseModel):
    title: str
    body: str
    creator: UserMiniOut

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    username: str
    email: str
    blogs: List[BlogOut] 

    class Config:
        orm_mode = True

class Blogs(BaseModel):
    blogs: List[BlogOut]
