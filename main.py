from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from routes.routes import routes_p 

app = FastAPI()
app.title = "KKM BD"
app.version = "0.0.1"
app.description = "API DESCRIPTION"

# Carga de variables de entorno
load_dotenv()

app.include_router(routes_p)

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
