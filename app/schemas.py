from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserOut(BaseModel):
    id :int
    email : EmailStr
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)

class PostCreate(PostBase):
    pass

# specify which data you want to receive and the type of it 
class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut  # This line indicates that the owner attribute of a Post instance will be of type UserOut, which is another Pydantic model defined later in the code. It allows you to include information about the owner of a post when returning post data in API responses.

    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    post : Post
    vote : int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email : EmailStr
    password : str


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)  # This line defines a field named dir in the Vote model, which is of type conint (constrained integer). The constraint le=1 means that the value of dir must be less than or equal to 1. This is useful for scenarios where you want to limit the possible values of dir to a specific range, such as 0 or 1, which could represent actions like "upvote" or "downvote" in a voting system.
