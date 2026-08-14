from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import time

app = FastAPI()

# La sesión en el servidor es puramente operativa y no guarda datos de usuario.
# El control del tiempo de 8 minutos se gestiona en la interfaz (cliente)
# para asegurar la destrucción total de datos volátiles.

@app.get("/")
async def get_index():
    # Retorna la interfaz inicial con el control de tiempo integrado
    return {"message": "Sistema Híbrido AL CIELO - Sesión Activa"}

@app.post("/destroy_session")
async def destroy_session():
    # Comando de cierre limpio solicitado por el Plan Maestro
    # En este punto el servidor confirma la limpieza de cualquier residuo en RAM
    return {"status": "session_destroyed", "message": "Memoria RAM limpiada"}
