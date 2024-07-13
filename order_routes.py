from fastapi import APIRouter,Depends,status
from fastapi_jwt_auth import AuthJWT
from models import User, Order, Product
from schemas import OrderModel, StatusOrderModel
from database import session,engine
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException


order_router = APIRouter(
    prefix='/order'
)

@order_router.get('/')
async def order(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    return {"message" : "Bu order route sahifasi"}