from typing import Optional
from pydantic import BaseModel

#Modelo de la tabla productos

class Product(BaseModel):
    marca: str 
    nombre: str
    talla: float
    precio: float
    numreferencia: str
    tipo: str
    proveedor: str
    categoria_id: int
    estado: bool 