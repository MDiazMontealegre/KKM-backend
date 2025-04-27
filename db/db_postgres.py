import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DATABASE = os.environ["POSTGRES_DATABASE"]

def get_db_connection():
    """Retorna una nueva conexión a la base de datos"""
    return psycopg2.connect(
        host=POSTGRES_HOST,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DATABASE,
        port=int(POSTGRES_PORT)
    )
