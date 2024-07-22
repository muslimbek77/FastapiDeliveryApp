from fastapi import FastAPI

from product_routes import product_router
from auth_routes import auth_router
from order_routes import order_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings, LoginModel

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_router)
app.include_router(order_router)
app.include_router(product_router)

@app.get('/')
async def root():
    return {"message": "Bu asosiy sahifa"}