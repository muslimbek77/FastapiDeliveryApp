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
        product_id = order.product_id,

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
        "product":{
            "id":new_order.product.id,
            "name":new_order.product.name,
            "price":new_order.product.price

        },
        "quantity":new_order.quantity,
        "order_statuses":new_order.order_statuses.value,
        "total_price": new_order.quantity*new_order.product.price
    }
        
    }

    response = data
    return jsonable_encoder(response)



@order_router.get('/list',status_code=status.HTTP_200_OK)
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
        custom_data = [{
            "id":order.id,
            "user":{
                "id":order.user.id,
                "username":order.user.username,
                "email":order.user.email
            },
        "product":{
            "id":order.product.id,
            "name":order.product.name,
            "price":order.product.price,
        
        },
        "quantity":order.quantity,
        "order_statuses":order.order_statuses.value,
        "total_price": order.quantity*order.product.price
        
    } 
        for order in orders]
        return jsonable_encoder(custom_data)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only super admin see orders")
    

@order_router.get('/{id}',status_code=status.HTTP_200_OK)
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


@order_router.get('/user/order',status_code=status.HTTP_200_OK)
async def get_user_orders(Authorize:AuthJWT=Depends()):
    """Get a requested user's order
    """
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Enter valid token")
    
    username = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == username).first()
    custom_data = [{
            "id":order.id,
            "user":{
                "id":order.user.id,
                "username":order.user.username,
                "email":order.user.email
            },
        "product":{
            "id":order.product.id,
            "name":order.product.name,
            "price":order.product.price,
        
        },
        "quantity":order.quantity,
        "order_statuses":order.order_statuses.value,
        "total_price": order.quantity*order.product.price}
        for order in user.orders
    ]

    return jsonable_encoder(custom_data)
    

# @order_router