from fastapi.responses import JSONResponse
import psycopg2
from psycopg2.extras import RealDictCursor
from db.db_postgres import get_db_connection
from models.product_model import Product

class ProductService:

    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        self.con = get_db_connection()  # Obtiene la conexión directamente
        if self.con is None:
            raise Exception("No se pudo establecer conexión con la base de datos")

    def get_products(self):
        """Consulta de todos los productos"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM producto")
                products = cursor.fetchall()
                return JSONResponse(
                    status_code=200,
                    content={"success": True, "message": "Productos listados correctamente", "data": products or []}
                )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al consultar los productos: {str(e)}", "data": None}
            )
        finally:
            if con:
                con.close()

    def get_product_by_id(self, product_id: int):
        """Consulta de un producto por su ID"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM producto WHERE id = %s", (product_id,))
                product = cursor.fetchone()

                if product:
                    return JSONResponse(
                        status_code=200,
                        content={"success": True, "message": "Producto encontrado", "data": product}
                    )
                else:
                    return JSONResponse(
                        status_code=404,
                        content={"success": False, "message": "Producto no encontrado", "data": None}
                    )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al consultar el producto: {str(e)}", "data": None}
            )
        finally:
            if con:
                con.close()

    def update_product(self, product_id: int, product_data: Product):
        """
        Actualiza los datos de un producto excepto el campo 'estado'.
        """
        try:
            #self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Verificar si el producto existe
                check_sql = "SELECT COUNT(*) FROM producto WHERE id=%s"
                cursor.execute(check_sql, (product_id,))
                result = cursor.fetchone()

                if result[0] == 0:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                # Actualizar campos (excepto estado)
                update_sql = """
                    UPDATE producto
                    SET marca=%s, nombre=%s, talla=%s, precio=%s, numreferencia=%s, proveedor=%s, tipo=%s, categoria_id=%s
                    WHERE id=%s
                """
                cursor.execute(update_sql, (
                    product_data.marca,
                    product_data.nombre,
                    product_data.talla,
                    product_data.precio,
                    product_data.numreferencia,
                    product_data.proveedor,
                    product_data.tipo,
                    product_data.categoria_id,
                    product_id
                ))
                self.con.commit()

                if cursor.rowcount > 0:
                    return JSONResponse(content={"success": True, "message": "Usuario actualizado correctamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=409)

        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al actualizar usuario: {str(e)}"}, status_code=500)
        finally:
            self.close_connection()

    def add_product(self, product_data: Product):
        """Agregar un nuevo producto"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor() as cursor:
                # Insertar nuevo producto
                cursor.execute(
                    """
                    INSERT INTO producto 
                    (marca, nombre, talla, precio, numreferencia, proveedor, tipo, categoria_id, estado) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        product_data.marca, product_data.nombre,
                        product_data.talla, product_data.precio, product_data.numreferencia,
                        product_data.proveedor, product_data.tipo, product_data.categoria_id, product_data.estado
                    )
                )
                new_product_id = cursor.fetchone()[0]
                con.commit()

                return JSONResponse(
                    status_code=201,
                    content={
                        "success": True,
                        "message": "Producto registrado correctamente.",
                        "data": {"product_id": new_product_id}
                    }
                )
        except Exception as e:
            if con:
                con.rollback()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": f"Error al registrar el producto: {str(e)}",
                    "data": None
                }
            )
        finally:
            if con:
                con.close()

    def toggle_product_status(self, product_id: int):
        con = None
        try:
            con = get_db_connection()  # Asegura una nueva conexión fresca
            with con.cursor() as cursor:
                # Obtener estado actual
                get_estado_sql = "SELECT estado FROM producto WHERE id=%s"
                cursor.execute(get_estado_sql, (product_id,))
                result = cursor.fetchone()

                if not result:
                    return JSONResponse(content={"success": False, "message": "Producto no encontrado."}, status_code=404)

                estado_actual = bool(result[0])
                nuevo_estado = not estado_actual

                update_sql = "UPDATE producto SET estado=%s WHERE id=%s"
                cursor.execute(update_sql, (nuevo_estado, product_id))
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
        """Llama al cierre de conexión de la base de datos."""
        self.con.close()