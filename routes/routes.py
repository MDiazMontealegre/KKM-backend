from fastapi import APIRouter, Body, Depends, HTTPException
from db.db_postgres import get_db_connection
from services.product_service import ProductService
from services.user_service import UserService
from services.rol_service import RolService
from models.product_model import Product
from models.user_model import User
from models.rol_model import Rol
from fastapi.responses import FileResponse
import csv


routes_p = APIRouter(prefix="/product", tags=["Product"])

product_service = ProductService()
product_model= Product

@routes_p.get("/get-products")
def get_all_products():
    return product_service.get_products()

@routes_p.get("/get-product/{product_id}")
def get_product(product_id: int):
    return product_service.get_product_by_id(product_id)

@routes_p.put("/update-product/{product_id}")
def update_product(product_id: int, product_data: Product):
    return product_service.update_product(product_id, product_data)

@routes_p.post("/add-product")
def add_product(product: Product):
    return product_service.add_product(product)

@routes_p.patch("/change-status/{product_id}")
def change_product_status(product_id: int):
    return product_service.toggle_product_status(product_id)

@routes_p.get("/export-products")
def export_products():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM producto")
    products = cursor.fetchall()
    header = [desc[0] for desc in cursor.description]

    filename = "productos_exportados.csv"
    filepath = f"/tmp/{filename}"

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(products)

    return FileResponse(filepath, filename=filename, media_type='text/csv')

#rutas usuario

routes_u = APIRouter(prefix="/user", tags=["User"])

user_service = UserService()
user_model= User

@routes_u.get("/get-users/")
def get_all_users():
    return user_service.get_users()

@routes_u.get("/get-user/{user_id}")
def get_user(user_id: int):
    return user_service.get_user_by_id(user_id)

@routes_u.post("/create-user/")
def create_user(user: User):
    return user_service.create_user(user)

@routes_u.put("/update-user/{user_id}")
def update_user(user_id: int, contrasena: str = Body(..., embed=True)):
    return user_service.update_user(user_id, contrasena)

@routes_u.patch("/change-status/{user_id}")
def change_user_status(user_id: int):
    return user_service.toggle_user_status(user_id)

@routes_u.get("/export-users")
def export_users():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT u.id, u.nombre as nombreu, u.correo, r.nombre as rol, u.estado 
        FROM usuario u
        JOIN rol r ON u.rol_id = r.id
    """)
    users = cursor.fetchall()
    header = [desc[0] for desc in cursor.description]

    filename = "usuarios_exportados.csv"
    filepath = f"/tmp/{filename}"

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(users)

    return FileResponse(filepath, filename=filename, media_type='text/csv')


# rutas rol

routes_r= APIRouter(prefix="/rol", tags=["Rol"])

rol_service= RolService()
rol_model= Rol

@routes_r.get("/get-roles/")
def get_all_roles():
    return rol_service.get_roles()

@routes_r.post("/create-rol/")
def create_rol(rol: Rol):
    return rol_service.create_role(rol)