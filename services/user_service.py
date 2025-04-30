from db.db_postgres import get_db_connection
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from fastapi.responses import JSONResponse
from models.user_model import User

class UserService:

    async def get_users(self):
        """Consulta de todos los usuarios"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM usuario")
                users = cursor.fetchall()
                return JSONResponse(
                    status_code=200,
                    content={"success": True, "message": "Usuarios listados correctamente", "data": users or []}
                )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al consultar los usuarios: {str(e)}", "data": None}
            )
        finally:
            if con:
                con.close()
    
    async def get_user_by_id(self, user_id: int):
        """Consulta de un usuario por su ID"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM usuario WHERE id = %s", (user_id,))
                user = cursor.fetchone()

                if user:
                    return JSONResponse(
                        status_code=200,
                        content={"success": True, "message": "Usuario encontrado", "data": user}
                    )
                else:
                    return JSONResponse(
                        status_code=404,
                        content={"success": False, "message": "Usuario no encontrado", "data": None}
                    )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al consultar el usuario: {str(e)}", "data": None}
            )
        finally:
            if con:
                con.close()

    async def create_user(self, user_data: User):
            """Crear un nuevo usuario"""
            conn= None
            try:
                conn = get_db_connection()
                with conn.cursor() as cursor:
                    # Verificar si ya existe el usuario
                    cursor.execute("SELECT * FROM usuario WHERE correo = %s", (user_data.correo,))
                    if cursor.fetchone():
                        cursor.close()
                        conn.close()
                        raise HTTPException(status_code=400, detail="Usuario ya registrado")
                    cursor.execute("SELECT * FROM rol WHERE id = %s", (user_data.rol_id))
                    if not cursor.fetchone():
                        raise HTTPException(status_code=400, detaiñ="El rol especificado no existe")
                    cursor.execute(
                        """
                        INSERT INTO usuario (nombre, correo, contrasena, rol_id, estado)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            user_data.nombre,
                            user_data.correo,
                            user_data.contrasena,
                            user_data.rol_id,
                            user_data.estado
                        )
                    )
                    new_user_id = cursor.fetchone()[0]
                    conn.commit()
                    cursor.close()
                    conn.close()

                    return JSONResponse(
                        status_code=201,
                        content={"success": True, "message": "Usuario registrado correctamente.", "data": {"user_id": new_user_id}}
                    )

            except Exception as e:
                if conn:
                    conn.rollback()
                return JSONResponse(
                    status_code=500,
                    content={"success": False, "message": f"Error al registrar usuario: {str(e)}", "data": None}
                )
    
    async def update_user(self, user_id: int, new_contrasena: int):
        """Actualizar la contraseña de un usuario"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor() as cursor:
                cursor.execute("UPDATE usuario SET contrasena = %s WHERE id = %s", (new_contrasena, user_id))
                con.commit()

                if cursor.rowcount > 0:
                    return JSONResponse(
                        status_code=200,
                        content={"success": True, "message": "Contraseña actualizada correctamente", "data": {"id": user_id, "nueva_contrasena": new_contrasena}}
                    )
                else:
                    return JSONResponse(
                        status_code=404,
                        content={"success": False, "message": "Usuario no encontrado para actualizar", "data": None}
                    )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al actualizar contraseña: {str(e)}", "data": None}
            )
        finally:
            if con:
                con.close()
