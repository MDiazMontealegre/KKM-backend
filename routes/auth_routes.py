from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.user_model import Usuario  # ORM creado
from db.db_postgres import get_db_connection  
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter(tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    correo: str
    contrasena: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db_connection)):
    user = db.query(Usuario).filter(Usuario.correo == request.correo).first()
    if not user or not pwd_context.verify(request.contrasena, user.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"message": "Login exitoso", "user_id": user.id}