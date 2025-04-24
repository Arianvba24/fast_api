from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr
    password : str


class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    class Config:
        from_attributes =  True

class UserLogin(BaseModel):
    email: EmailStr
    password : str

class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True
    # owner_id : int


class PostCreate(PostBase):
    pass

# class Post(BaseModel):
#     title: str
#     created_at : datetime
#     owner_id : int
#     owner : UserOut

#     class Config:
#         from_attributes = True

class Post(PostBase):
    id_value : int
    created_at : datetime
    owner_id : int
    owner : UserOut

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id_value : Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir : conint(le=1)

# class PostCreate(PostBase):
#     pass

# class PostUpdate(PostBase):
#     pass


# class Post(BaseModel):
#     id_value : int
#     title: str
#     content : str
#     published : bool
#     created_at : datetime

#     class Config:
#         from_attributes =  True

