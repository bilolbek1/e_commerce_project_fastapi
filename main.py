from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
import auth_routes
import product_routes
import category_routes
from schemas import Settings


@AuthJWT.load_config
def get_config():
    return Settings()


app=FastAPI()


app.include_router(auth_routes.auth_router)
app.include_router(product_routes.product_router)
app.include_router(category_routes.category_router)

@app.get('/')
async def home():
    return {"message": "Hello guys this is home page"}