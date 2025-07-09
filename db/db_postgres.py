import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DATABASE = os.environ["POSTGRES_DATABASE"]

# Construir la URL de conexión desde variables de entorno

DATABASE_URL = "postgresql://db_kkm_user:q14Z24jCqyNmmtHQRkUjsrVfqcT8zVXz@dpg-d1mmn5jipnbc73c4l380-a.oregon-postgres.render.com/db_kkm"

# Crear el motor SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener sesión en las rutas
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Usar en servicios que requieren cursor (psycopg2)
def get_db_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DATABASE,
        port=int(POSTGRES_PORT)
    )