from models.rol_model import Rol
from pydantic import BaseModel
from typing import Union

#Modelo de la tabla usuarios

class User(BaseModel):
    nombre: str
    correo: str
    contrasena: str
    rol_id: Union[int, Rol]
    estado: bool 