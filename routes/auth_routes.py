from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.user_model import Usuario  # ORM creado
from db.db_postgres import get_db_session  
from schemas.login_schema import LoginSchema

router = APIRouter()

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db_session)):
    try:
        print("✅ Iniciando login con:", data.correo)

        user = db.query(Usuario).filter(Usuario.correo == data.correo).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        if user.contrasena != data.contrasena:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        
        return {"mensaje": "Inicio de sesión exitoso", "usuario_id": user.id}

    except Exception as e:
        print("💥 Error en login:", str(e))  # Log real del error
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    