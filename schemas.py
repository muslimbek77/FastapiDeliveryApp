from pydantic import BaseModel, Field
from typing import Optional

class SingUpModel(BaseModel):
    id: Optional[int]  # Example: 1
    username: str      # Example: 'mohirdev'
    email: str         # Example: 'mohirdev.praktikum@gmail.com'
    password: str      # Example: 'password12345'
    is_staff: Optional[bool] = False   # Example: False
    is_active: Optional[bool] = True  # Example: True

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'mohirdev',
                'email': 'mohirdev.praktikum@gmail.com',
                'password': 'password12345',
                'is_staff': False,
                'is_active': True
            }
        }

class Settings(BaseModel):
    authjwt_secret_key:str = '26b092890d86493464b8bf8b6b233e12c711b327a5cc9c39c10ee046ba805c7a'


class LoginModel(BaseModel):
    userame_or_email: str    # Example: 'mohirdev'
    password: str    # Example: 'password12345'

class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_satatus:Optional[str] = 'PENDING'
    user_id:Optional[int]
    product_id:Optional[int]
    class Config:
        orm_model = True
        schema_extra = {
            "example":{
                "quantity":2,

            }
        }


class StatusOrderModel(BaseModel):
    order_statuses:Optional[str] = 'PENDING'
    class Config:
        orm_model = True
        schema_extra = {
            "example":{
                "order_satuses":"Pending",

            }
        }

    