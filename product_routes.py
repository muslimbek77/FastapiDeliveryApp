from fastapi import APIRouter,Depends,status
from fastapi_jwt_auth import AuthJWT
from models import User,  Product
from schemas import ProductModel, StatusOrderModel
from database import session,engine
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException


product_router = APIRouter(
    prefix='/product'
)

session = session(bind=engine)

@product_router.post('/create',status_code=status.HTTP_201_CREATED)
async def create_product(product:ProductModel,Authorize:AuthJWT=Depends()):
        # Create new product
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Enter valid token")
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    if current_user.is_staff:
        new_product = Product(
            name=product.name,
            price=product.price
        )
        session.add(new_product)
        session.commit()
        data = {
            "success":True,
            "code":201,
            "message":"Product is created successfully",
            "data":{
                "id":new_product.id,
                "name":new_product.name,
                "price":new_product.price
            }
        }
        return jsonable_encoder(data)
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only admin can add product")


@product_router.get('/list',status_code=status.HTTP_200_OK)
async def list_all_products(Authorize:AuthJWT=Depends()):
    # Bu rote barcha mahsulotlar ro'yhatini chiqarib beradi
        # Get an order by its ID
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Enter valid token")
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    
    products = session.query(Product).all()
    custom_data = [
        {
                "id":product.id,
                "name":product.name,
                "price":product.price
            }
            for product in products
            ]
    return jsonable_encoder(custom_data)
    

@product_router.get('/{id}',status_code=status.HTTP_200_OK)
async def get_product_by_id(id:int, Authorize:AuthJWT=Depends()):
    # Get an order by its ID
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Enter valid token")
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            custom_data = {
                    "id":product.id,
                    "name":product.name,
                    "price":product.price
                }

            return jsonable_encoder(custom_data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found id {id}")


    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only super admin see this order")

    
@product_router.get('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_by_id(id:int,Authorize:AuthJWT=Depends()):
    #Bu endpoint mahsulotni o'chirish uchun ishlatiladi
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Enter valid token")
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
        
    product = session.query(Product).filter(Product.id == id).first()
    if current_user.is_staff:
        if product:
            session.delete(product)
            session.commit()
            data={
                "success":True,
                "code":200,
                "message": f"Product with ID {id} has been deleted"
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found this ID {id}")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only superadmin product delete")


@product_router.put('/update/{id}',status_code=status.HTTP_200_OK)
async def put_product_by_id(id:int,update_data:ProductModel,Authorize:AuthJWT=Depends()):
    #Bu endpoint mahsulotni yangilash uchun ishlatiladi
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Enter valid token")
    
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    
    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            #update product
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(product, key, value)
            session.commit()
            data={
                "success":True,
                "code":200,
                "message": f"Product with ID {id} has been updated",
                "data":{
                    "id":product.id,
                    "name":product.name,
                    "price":product.price
                }
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found this ID {id}")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only superadmin product update")

