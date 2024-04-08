from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional, Union

# --- find user schema ---

class FindUser(BaseModel):
    name: str

# -- user schema -- 

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResp(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class GetUsers(UserResp):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# -- post schema -- 

class Books(BaseModel):
    book_name: str
    author: str
    published: bool = True
    sales: str

class CreatePost(Books):
    pass

class UpdatePost(Books):
    pass

class UpdateSales(BaseModel):
    sales: str

class PublishedBook(BaseModel):
    published: bool

class PatchPublishedBooks(BaseModel):
    published: bool

# response for createPosts 
class CreatePostResp(Books):
    user_id: int
    created_at: datetime
    username: str
    user: UserResp

    class Config:
        orm_mode = True

class GetPost(CreatePostResp):
    pass

# -- Token && Token Data scheme --

class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

# -- routes scheme --

class GetAllRoutes(BaseModel):
    get_post: str = "http://127.0.0.1:8000/posts"
    create_post: str = "http://127.0.0.1:8000/posts"
    update_post: str = "http://127.0.0.1:8000/update/{user_id}"
    delete_post: str = "http://127.0.0.1:8000/posts/delete/{user_id}"
    patch_post: str = "http://127.0.0.1:8000/patch/{user_id}"
    
# -- like schema --

class Like(BaseModel):
    post_id: int
    # like: conint(le=1)
    like: int
    
    def check(self):
        if self.like > 1 or self.like < 0:
            return None 
        return self.like 
    
