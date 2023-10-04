from pydantic import BaseModel, BaseSettings
from typing import Optional



class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]


    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "username": "string",
                "first_name": "firstname",
                "last_name": "lastname",
                "email": "string@gamil.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }



class Settings(BaseModel):
    authjwt_secret_key: str = '61a9d13e596d84151a082c1ed8f39cb9c20334449703a56033eed4ec54900c83'


class LoginModel(BaseModel):
    username: str
    password: str




class ProductModel(BaseModel):
    id: Optional[int]
    name: str
    description: str
    old_price: int
    new_price: int
    category_id: Optional[int]
    user_id: Optional[int]



class CategoryModel(BaseModel):
    id: Optional[int]
    name: str




class ProfileModel(BaseModel):
    id: Optional[int]
    username: str
    first_name: str
    last_name: str
    email: Optional[str]
    is_active: Optional[bool]

































