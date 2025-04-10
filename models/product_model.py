from typing import Optional
from pydantic import BaseModel

#Modelo de la tabla productos

class Product(BaseModel):
    categoria: str
    marca: str 
    nombre: str
    talla: float
    precio: float
    numreferencia: str
    proveedor: str
    stock: int
    estado: Optional[int]=1    