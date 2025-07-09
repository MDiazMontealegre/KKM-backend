from db.db_postgres import get_db_connection
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from psycopg2.extras import RealDictCursor
from fastapi.responses import JSONResponse
from models.user_model import User

class UserService:

    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        self.con = get_db_connection()
        if self.con is None:
            raise Exception("No se pudo establecer conexión con la base de datos")

    def get_users(self):
        """Consulta de todos los usuarios"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                sql= """SELECT u.id, u.nombre as nombreu, u.correo, u.contrasena, r.nombre, u.estado 
                        FROM usuario u
                        JOIN rol r ON u.rol_id = r.id"""
                cursor.execute(sql)
                users = cursor.fetchall()
                return JSONResponse(content={"success": True, "data": users}, status_code=200)
                
        except Exception as e:
            return JSONResponse(content={"success": False, "message": f"Error al consultar bolsillos: {str(e)}"}, status_code=500)
    
    def get_user_by_id(self, user_id: int):
        """Consulta de un usuario por su ID"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                sql = """SELECT u.nombre as nombreu, u.correo, u.contrasena, r.nombre, u.estado 
                        FROM usuario u
                        JOIN rol r ON u.rol_id = r.id
                        WHERE r.id = %s"""
                cursor.execute(sql, (user_id,))
                user = cursor.fetchone()

                if user:
                    return JSONResponse(content={"success": True, "data": user}, status_code=200)
                    
                else:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)
        except Exception as e:
            return JSONResponse(content={"success": False, "message": f"Error al consultar el usuario: {str(e)}"}, status_code=500)

    def create_user(self, user_data: User):
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
                    
                    sql = "INSERT INTO usuario (nombre, correo, contrasena, rol_id, estado) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (user_data.nombre, user_data.correo, user_data.contrasena, user_data.rol_id, user_data.estado))
                    conn.commit()

                    if cursor.lastrowid:
                        return JSONResponse(content={"success": True, "message": "Usuario creado correctamente.", "id": cursor.lastrowid}, status_code=201)
                    else:
                        return JSONResponse(content={"success": False, "message": "No se pudo crear el usuario."}, status_code=400)
            except Exception as e:
                self.con.rollback()
                return JSONResponse(content={"success": False, "message": f"Error al crear Usuario: {str(e)}"}, status_code=500)          
    
    def update_user(self, user_id: int, new_contrasena: int):
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

    def toggle_user_status(self, user_id: int):
        con = None
        try:
            con = get_db_connection()  # Asegura una nueva conexión fresca
            with con.cursor() as cursor:
                # Obtener estado actual
                get_estado_sql = "SELECT estado FROM usuario WHERE id=%s"
                cursor.execute(get_estado_sql, (user_id,))
                result = cursor.fetchone()

                if not result:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                estado_actual = bool(result[0])
                nuevo_estado = not estado_actual

                update_sql = "UPDATE usuario SET estado=%s WHERE id=%s"
                cursor.execute(update_sql, (nuevo_estado, user_id))
                con.commit()

                return JSONResponse(content={
                    "success": True,
                    "message": "Estado actualizado correctamente.",
                    "estado_actual": estado_actual,
                    "nuevo_estado": nuevo_estado
                }, status_code=200)

        except Exception as e:
            if con:
                con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al cambiar estado: {str(e)}"}, status_code=500)

        finally:
            if con:
                con.close()

    def close_connection(self):
        """Cierra la conexión con la base de datos."""
        if self.con:
            self.con.close()