from typing import Optional
from pydantic import BaseModel

#Modelo de la tabla rol

class Rol(BaseModel):
    nombre: str