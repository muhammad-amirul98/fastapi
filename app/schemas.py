from pydantic import BaseModel, EmailStr
from datetime import datetime
import sqlalchemy
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel): #this is what is known as a schema, these are referenced in our post or update functions where we want the input to be of this specific model
    title: str
    content: str
    published: bool = True #whether the post is published or draft, this field is optional since a value is already provided default
    # rating: Optional[int] = None 

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Post(PostBase): #only returning these items to the user and not showing id and timestamp
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    email: EmailStr #pydantic does automatic email validation
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
    dir: conint(le=1)