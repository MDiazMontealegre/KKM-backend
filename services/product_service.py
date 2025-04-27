from fastapi.responses import JSONResponse
import psycopg2
from psycopg2.extras import RealDictCursor
from db.db_postgres import get_db_connection
from models.product_model import Product

class ProductService:

    async def get_products(self):
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

    async def get_product_by_id(self, product_id: int):
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

    async def update_stock(self, product_id: int, new_stock: int):
        """Actualizar el stock de un producto"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor() as cursor:
                cursor.execute("UPDATE producto SET stock = %s WHERE id = %s", (new_stock, product_id))
                con.commit()

                if cursor.rowcount > 0:
                    return JSONResponse(
                        status_code=200,
                        content={"success": True, "message": "Stock actualizado correctamente", "data": {"id": product_id, "nuevo_stock": new_stock}}
                    )
                else:
                    return JSONResponse(
                        status_code=404,
                        content={"success": False, "message": "Producto no encontrado para actualizar", "data": None}
                    )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al actualizar el stock: {str(e)}", "data": None}
            )
        finally:
            if con:
                con.close()

    async def add_product(self, product_data: Product):
        """Agregar un nuevo producto o actualizar el stock si ya existe"""
        con = None
        try:
            con = get_db_connection()
            with con.cursor() as cursor:
                # Verificar si el producto ya existe
                cursor.execute(
                    "SELECT id, stock FROM producto WHERE marca = %s AND nombre = %s AND talla = %s",
                    (product_data.marca, product_data.nombre, product_data.talla)
                )
                existing_product = cursor.fetchone()

                if existing_product:
                    existing_product_id = existing_product[0]
                    existing_stock = existing_product[1]
                    new_stock = existing_stock + product_data.stock

                    cursor.execute(
                        "UPDATE producto SET stock = %s WHERE id = %s",
                        (new_stock, existing_product_id)
                    )
                    con.commit()

                    return JSONResponse(
                        status_code=200,
                        content={"success": True, "message": "Producto existente, stock actualizado.", "data": {"product_id": existing_product_id, "nuevo_stock": new_stock}}
                    )
                else:
                    # Insertar nuevo producto
                    cursor.execute(
                        """
                        INSERT INTO producto 
                        (marca, nombre, talla, precio, numreferencia, proveedor, stock, estado) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            product_data.marca, product_data.nombre,
                            product_data.talla, product_data.precio, product_data.numreferencia,
                            product_data.proveedor, product_data.stock, product_data.estado
                        )
                    )
                    new_product_id = cursor.fetchone()[0]
                    con.commit()

                    return JSONResponse(
                        status_code=201,
                        content={"success": True, "message": "Producto registrado correctamente.", "data": {"product_id": new_product_id}}
                    )
        except Exception as e:
            if con:
                con.rollback()
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al registrar o actualizar el producto: {str(e)}", "data": None}
            )
        finally:
            if con:
                con.close()