from typing import Optional
from pydantic import BaseModel

#Modelo de la tabla usuarios

class User(BaseModel):
    nombre: str
    correo: str
    contrasena: str
    rol_id: int
    estado: bool 