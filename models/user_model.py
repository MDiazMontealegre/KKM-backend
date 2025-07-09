from models.rol_model import Rol
from pydantic import BaseModel
from typing import Union
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

#Modelo de la tabla usuarios

class User(BaseModel):
    nombre: str
    correo: str
    contrasena: str
    rol_id: Union[int, Rol]
    estado: bool 

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    contrasena = Column(String, nullable=False)
    rol_id = Column(Integer, ForeignKey("rol.id"))  
    estado = Column(Boolean, default=True)