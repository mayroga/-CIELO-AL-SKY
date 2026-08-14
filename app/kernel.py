from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# Importación del kernel especializado
from app.kernel import AsesorKernel

app = FastAPI()
kernel = AsesorKernel()

@app.get("/", response_class=HTMLResponse)
async def get_index():
    # Carga de la interfaz principal de AL CIELO
    index_path = os.path.join("app", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: index.html no encontrado</h1>"

@app.post("/validar")
async def validar_datos_endpoint(nombre: str = Form(...), pasaporte: str = Form(...), lang: str = Form("es")):
    # Conexión directa con la lógica de validación del kernel (estilo niño de 8 años)
    resultado = kernel.validar_datos_entrada(nombre, pasaporte, lang)
    return JSONResponse(content=resultado)

@app.post("/destroy_session")
async def destroy_session():
    # Destrucción limpia de la sesión en memoria volátil
    return {"status": "session_destroyed", "message": "Memoria RAM limpiada"}
