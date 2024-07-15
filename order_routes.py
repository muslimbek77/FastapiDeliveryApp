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

session = session(bind=engine)


@order_router.get('/')
async def order(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    return {"message" : "Bu order route sahifasi"}

@order_router.post('/make',status_code=status.HTTP_201_CREATED)
async def make_order(order:OrderModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        quantity = order.quantity,
        # product = order.product_id,

    )
    new_order.user = user
    session.add(new_order)
    session.commit()

    data = {
        "success":True,
        "code":201,
        "message":"Order is created successfully",
        "data":{
        "id":new_order.id,
        "quantity":new_order.quantity,
        "order_statuses":new_order.order_statuses,
    }
        
    }

    response = data
    return jsonable_encoder(response)



@order_router.get('/list')
async def list_all_order(Authorize:AuthJWT=Depends()):
    #Bu yerda barcha buyurmalar bo'ladi
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Enter valid token")
    
    current_user =Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only super admin see orders")
    

@order_router.get('/{id}')
async def get_orer_by_id(id:int, Authorize:AuthJWT=Depends()):
    # Get an order by its ID
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Enter valid token")
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        
        order = session.query(Order).filter(Order.id == id).first()
        if order:

            return jsonable_encoder(order)
        else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found id {id}")

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only super admin see this order")

    