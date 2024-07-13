from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings, LoginModel


app = FastAPI()
app.include_router(auth_router)
app.include_router(order_router)


@app.get('/')
async def root():
    return {'message' : "Fastapi loyihamiz ishladi."}

@AuthJWT.load_config
def get_config():
    return Settings()