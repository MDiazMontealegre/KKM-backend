from fastapi import APIRouter, Body
from services.product_service import ProductService
from models.product_model import Product

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