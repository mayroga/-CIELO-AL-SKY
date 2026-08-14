from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
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
    return "<h1>Ay, caramba: No encontramos la casita de inicio (index.html).</h1>"

@app.get("/frases_render")
async def obtener_frases_render(lang: str = "es"):
    if lang == "es":
        return {"frases": kernel.frases_render_es}
    return {"frases": kernel.frases_render_en}

@app.get("/frases_respiracion")
async def obtener_frases_respiracion(lang: str = "es"):
    if lang == "es":
        return {"frases": kernel.frases_respiracion_es}
    return {"frases": kernel.frases_respiracion_en}

@app.get("/opciones_vuelo")
async def obtener_opciones_vuelo_endpoint(lang: str = "es"):
    resultado = kernel.obtener_opciones_vuelo(lang)
    return JSONResponse(content=resultado)

@app.post("/validar")
async def validar_datos_endpoint(nombre: str = Form(...), pasaporte: str = Form(...), lang: str = "es"):
    resultado = kernel.validar_datos_entrada(nombre, pasaporte, lang)
    return JSONResponse(content=resultado)

@app.post("/traducir_itinerario")
async def traducir_itinerario_endpoint(origen: str = Form(...), escala: str = Form(...), destino: str = Form(...), horas_escala: str = Form(...), lang: str = "es"):
    resultado = kernel.traducir_itinerario(origen, escala, destino, horas_escala, lang)
    return JSONResponse(content=resultado)

@app.post("/destroy_session")
async def destroy_session():
    return {"status": "session_destroyed", "message": "Memoria limpiada con éxito"}
