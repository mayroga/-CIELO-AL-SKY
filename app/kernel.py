from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from app.kernel import AsesorKernel

app = FastAPI()
kernel = AsesorKernel()

@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_path = os.path.join("app", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: index.html no encontrado</h1>"

@app.post("/validar")
async def validar_datos_endpoint(nombre: str = Form(...), pasaporte: str = Form(...), lang: str = Form("es")):
    resultado = kernel.validar_datos_entrada(nombre, pasaporte, lang)
    return JSONResponse(content=resultado)

@app.post("/traducir_itinerario")
async def traducir_itinerario_endpoint(origen: str = Form(...), escala: str = Form(...), destino: str = Form(...), horas_escala: str = Form(...), lang: str = Form("es")):
    resultado = kernel.traducir_itinerario(origen, escala, destino, horas_escala, lang)
    return JSONResponse(content=resultado)

@app.post("/destroy_session")
async def destroy_session():
    return {"status": "session_destroyed", "message": "Memoria RAM limpiada"}
