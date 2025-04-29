from fastapi import APIRouter, Body, Depends, HTTPException
from services.product_service import ProductService
from services.user_service import UserService
from models.product_model import Product
from models.user_model import User


routes_p = APIRouter(prefix="/product", tags=["Product"])

product_service = ProductService()

@routes_p.get("/get-products")
async def get_all_products():
    return await product_service.get_products()

@routes_p.get("/get-product/{product_id}")
async def get_product(product_id: int):
    return await product_service.get_product_by_id(product_id)

@routes_p.put("/update-stock/{product_id}")
async def update_product_stock(product_id: int, stock: int = Body(..., embed=True)):
    return await product_service.update_stock(product_id, stock)

@routes_p.post("/add-product")
async def add_product(product: Product):
    return await product_service.add_product(product)

#rutas usuario

routes_u = APIRouter(prefix="/user", tags=["User"])

user_service = UserService()

@routes_u.get("/get-users/")
async def get_all_users():
    return await user_service.get_users()

@routes_u.get("/get-user/{user_id}")
async def get_user(user_id: int):
    return await user_service.get_user_by_id(user_id)

@routes_u.post("/create-user/")
async def create_user(user: User):
    return await user_service.create_user(user)

@routes_u.put("/update-user/{user_id}")
async def update_user(user_id: int, contrasena: str = Body(..., embed=True)):
    return await user_service.update_user(user_id, contrasena)




