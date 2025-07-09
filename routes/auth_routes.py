from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.user_model import Usuario  # ORM creado
from db.db_postgres import get_db_connection  
from schemas.login_schema import LoginSchema

router = APIRouter()

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db_connection)):
    usuario = db.query(Usuario).filter(Usuario.correo == data.correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if usuario.contrasena != data.contrasena:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    return {"mensaje": "Inicio de sesión exitoso", "usuario_id": usuario.id}