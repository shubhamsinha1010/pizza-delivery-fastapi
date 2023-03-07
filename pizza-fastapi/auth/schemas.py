from pydantic import BaseModel
from typing import Optional


class SignUpSchema(BaseModel):
    """Schema which specifies the fields required as an input"""
    id:Optional[int]
    username:str
    email:str
    password:str
    profile_pic: Optional[str]
    is_staff:Optional[bool]
    is_active:Optional[bool]


    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "username":"johndoe",
                "email":"johndoe@gmail.com",
                "password":"password",
                "is_staff":False,
                "is_active":True,
                "profile_pic": "/home/root255/fastapi-pizza/pizza-fastapi/static/Screenshot from 2022-10-06 22-11-17.png"
            }
        }




class LoginSchema(BaseModel):
    """Schema which specifies the fields required as an input"""
    username:str
    password:str
