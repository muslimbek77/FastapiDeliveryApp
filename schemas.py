from pydantic import BaseModel
from typing import Optional

class SingUpModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example':{
            'username' : 'mohirdev',
            'email':'mohirdev.praktikum@gmail.com',
            'password':'password12345',
            'is_staff':False,
            'is_active':True
        }
        }