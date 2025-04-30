from fastapi import APIRouter, Body, Depends, HTTPException
from services.product_service import ProductService
from services.user_service import UserService
from services.rol_service import RolService
from models.product_model import Product
from models.user_model import User
from models.rol_model import Rol


routes_p = APIRouter(prefix="/product", tags=["Product"])

product_service = ProductService()

@routes_p.get("/get-products")
async def get_all_products():
    return await product_service.get_products()

@routes_p.get("/get-product/{product_id}")
async def get_product(product_id: int):
    return await product_service.get_product_by_id(product_id)

@routes_p.put("/update-product/{product_id}")
async def update_product(product_id: int, product_data: Product):
    return await product_service.update_product(product_id, product_data)

@routes_p.post("/add-product")
async def add_product(product: Product):
    return await product_service.add_product(product)

@routes_p.patch("/change-status/{product_id}")
async def change_product_status(product_id: int):
    return await product_service.toggle_product_status(product_id)

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


# rutas rol

routes_r= APIRouter(prefix="/rol", tags=["Rol"])

rol_service= RolService()

@routes_r.get("/get-roles/")
async def get_all_roles():
    return await rol_service.get_roles()

@routes_r.post("/create-rol/")
async def create_rol(rol: Rol):
    return await rol_service.create_role(rol)