from fastapi.responses import JSONResponse
import pymysql
import pymysql.cursors
from db.db_mysql import get_db_connection
from models.product_model import Product

class ProductService:
    def __init__(self):
        self.con=get_db_connection()
        if self.con is None:
            print("No se pudo establecer conexión a la BD")
    
    async def get_products(self):
        """Consulta de los productos de la tabla producto"""
        try:
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM producto")
                products=cursor.fetchall()

                return JSONResponse(
                    status_code=200,
                    content={
                        "success": True,
                        "message": "Productos listados correctamente",
                        "data": products if products else []
                    }
                )
        except Exception as e:
            return JSONResponse(
                    status_code=500,
                    content={
                        "success": False,
                        "message": f"Error al consultar los productos {str(e)}",
                        "data": None
                    }
                )
        
    async def get_product_by_id(self, product_id):
        """Consulta de los productos de la tabla Producto por su id"""
        try:
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql= "SELECT * FROM producto WHERE id = %s"
                cursor.execute(sql, (product_id,))
                product=cursor.fetchone()
                print(product)

                if product: 

                    return JSONResponse(
                        status_code=200,
                        content={
                            "success": True,
                            "message": "Producto encontrado",
                            "data": product
                        }
                )
                else:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "success": True,
                            "message": "Producto no encontrado",
                            "data": None
                        }
                )

        except Exception as e:
            return JSONResponse(
                    status_code=500,
                    content={
                        "success": False,
                        "message": f"Error al consultar el producto {str(e)}",
                        "data": None
                    }
                )
    
    async def update_stock(self, product_id: int, new_stock: int):
        """Actualizar el stock de un producto por su ID"""
        try:
            with self.con.cursor() as cursor:
                sql = "UPDATE producto SET stock = %s WHERE id = %s"
                cursor.execute(sql, (new_stock, product_id))
                self.con.commit()

                if cursor.rowcount > 0:
                    return JSONResponse(
                        status_code=200,
                        content={
                            "success": True,
                            "message": "Stock actualizado correctamente",
                            "data": {"id": product_id, "nuevo_stock": new_stock}
                        }
                    )
                else:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "success": False,
                            "message": "Producto no encontrado para actualizar",
                            "data": None
                        }
                    )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": f"Error al actualizar el stock: {str(e)}",
                    "data": None
                }
            )
    
    async def add_product(self, product_data: Product):
        """Creación o actualización de stock si el producto ya existe con los mismos atributos clave"""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Verificar si ya existe un producto con las mismas características
                check_sql = """SELECT id, stock FROM producto WHERE categoria = %s AND marca = %s AND nombre = %s AND talla = %s"""
                cursor.execute(check_sql, (
                    product_data.categoria, 
                    product_data.marca, 
                    product_data.nombre, 
                    product_data.talla, 
                ))
                existing_product = cursor.fetchone()

                if existing_product:
                    # Si existe, actualizamos el stock sumando el nuevo
                    new_stock = existing_product[1] + product_data.stock
                    update_sql = "UPDATE producto SET stock = %s WHERE id = %s"
                    cursor.execute(update_sql, (new_stock, existing_product[0]))
                    self.con.commit()

                    return JSONResponse(
                        status_code=200,
                        content={
                            "success": True,
                            "message": "Producto existente, stock actualizado.",
                            "data": {"product_id": existing_product[0], "nuevo_stock": new_stock}
                        }
                    )
                else:
                    # Si no existe, insertamos como nuevo producto
                    insert_sql = """
                        INSERT INTO producto 
                        (categoria, marca, nombre, talla, precio, numreferencia, proveedor, stock, estado) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_sql, (
                        product_data.categoria, product_data.marca, product_data.nombre,
                        product_data.talla, product_data.precio, product_data.numreferencia,
                        product_data.proveedor, product_data.stock, product_data.estado
                    ))
                    self.con.commit()

                    if cursor.lastrowid:
                        return JSONResponse(
                            status_code=201,
                            content={
                                "success": True,
                                "message": "Producto registrado correctamente.",
                                "data": {"product_id": cursor.lastrowid}
                            }
                        )
                    else:
                        return JSONResponse(
                            status_code=400,
                            content={
                                "success": False,
                                "message": "No se pudo registrar el producto.",
                                "data": None
                            }
                        )

        except Exception as e:
            self.con.rollback()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": f"Error al registrar o actualizar el producto: {str(e)}",
                    "data": None
                }
            )