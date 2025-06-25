from dotenv import load_dotenv
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from openpyxl import Workbook
import os
from routes.routes import routes_p 
from routes.routes import routes_u
from routes.routes import routes_r


app = FastAPI()
app.title = "KKM BD"
app.version = "0.0.1"
app.description = "API DESCRIPTION"

# Carga de variables de entorno
load_dotenv()

app.include_router(routes_p)
app.include_router(routes_u)
app.include_router(routes_r)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "UPDATE"],
    allow_headers=["*"]
)

@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="DEFAULT API",
    tags=["APP"]
)
def message():
    """Home API"""
    return HTMLResponse("<h1> Ejercicio de Pruebas </h1>")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.get("/generar-reporte")
def generar_reporte():
    wb = Workbook()
    ws = wb.active
    ws.title = "Inventario"

    # Cabeceras
    ws.append(["Marca", "Nombre", "Talla", "Precio", "Num. Referencia", "Proveedor", "Tipo", "Categoria_id"])

    # Simula extracción de base de datos
    from db import get_db_connection
    db = get_db_connection()
    productos = db.execute("SELECT marca, nombre, talla, precio, referencia, proveedor, tipo, categoria_id FROM productos").fetchall()

    for prod in productos:
        ws.append(prod)

    ruta_archivo = "reporte_inventario.xlsx"
    wb.save(ruta_archivo)

    return FileResponse(path=ruta_archivo, filename="reporte_inventario.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))