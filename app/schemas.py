from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional

'''
These Pydantic models represent data model classes 
'''
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True 

class Post(PostBase):  # this is to response schema model
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut  # here the datatype is pydantic model and need to specify that model before use.

    class Config:
        orm_mode = True  # this Sql-Pydantic convertor needs to be added to convert sqlalchemy model to Pydantic model. 

class PostOut(BaseModel):  # this is to response schema model
    Post: Post
    votes: int
   
    class Config:
        orm_mode = True  # this Sql-Pydantic convertor needs to be added to convert sqlalchemy model to Pydantic model. 

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)  # this is expects 0 or 1. grater than or equal 0, less than or equal 1