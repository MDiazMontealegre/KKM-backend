from db.db_postgres import get_db_connection
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor

class UserService:

    @staticmethod
    def create_user(user_data: dict):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Verificar si ya existe el username
        cur.execute("SELECT * FROM usuario WHERE nombre = %s", (user_data["nombre"],))
        if cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Nombre de usuario ya registrado")

        query = """
            INSERT INTO usuario (nombre, correo, contrasena, rol_id, estado)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *;
        """
        cur.execute(query, (
            user_data["nombre"],
            user_data["correo"],
            user_data["contrasena"],
            user_data["rol_id"],
            user_data["estado"]
        ))

        new_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return new_user

    @staticmethod
    def update_user(user_id: int, user_update: dict):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM usuario WHERE id = %s", (user_id,))
        user = cur.fetchone()
        if not user:
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        fields = []
        values = []

        for key, value in user_update.items():
            fields.append(f"{key} = %s")
            values.append(value)

        values.append(user_id)
        set_clause = ", ".join(fields)

        cur.execute(f"UPDATE usuario SET {set_clause} WHERE id = %s RETURNING *;", tuple(values))

        updated_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return updated_user

    @staticmethod
    def get_users():
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM usuario")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return users

    @staticmethod
    def get_user_by_id(user_id: int):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM usuario WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
