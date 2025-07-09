from db.db_postgres import get_db_connection
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from fastapi.responses import JSONResponse
from models.rol_model import Rol

class RolService:

    def get_roles(self):
        """Consulta de todos los roles"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM rol")
                roles = cursor.fetchall()
                return JSONResponse(
                    status_code=200,
                    content={"success": True, "message": "Roles listados correctamente", "data": roles or []}
                )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al consultar los roles: {str(e)}", "data": None}
            )
        finally:
            if con:
                con.close()

    def create_role(self, role_data: Rol):
        """Crear un nuevo rol"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO rol (nombre)
                    VALUES (%s)
                    RETURNING id
                    """,
                    (role_data.nombre,)
                )
                new_role_id = cursor.fetchone()[0]
                con.commit()

                return JSONResponse(
                    status_code=201,
                    content={"success": True, "message": "Rol creado correctamente.", "data": {"rol_id": new_role_id}}
                )
        except Exception as e:
            if con:
                con.rollback()
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al crear rol: {str(e)}", "data": None}
            )
        finally:
            if con:
                con.close()