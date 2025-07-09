from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user_model import Usuario
from db.db_postgres import get_db_connection  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def actualizar_contrasenas():
    db: Session = next(get_db_connection())
    usuarios = db.query(Usuario).all()

    actualizados = 0
    for u in usuarios:
        if not u.contrasena.startswith("$2b$"):
            print(f"Actualizando contraseña para usuario: {u.correo}")
            u.contrasena = pwd_context.hash(u.contrasena)
            actualizados += 1

    if actualizados:
        db.commit()
        print(f"✔️ {actualizados} contraseñas hasheadas con bcrypt.")
    else:
        print("✅ Todas las contraseñas ya estaban hasheadas.")

if __name__ == "__main__":
    actualizar_contrasenas()