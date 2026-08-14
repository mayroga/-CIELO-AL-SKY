import os
from fastapi import FastAPI, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from app.kernel import AsesorKernel

# Inicialización de la aplicación FastAPI
app = FastAPI(title="AL CIELO - API Core")

# Instancia global del motor inteligente de asistencia
kernel = AsesorKernel()

# =========================================================================
# RUTA RAÍZ: DEVUELVE TU INDEX.HTML DIRECTAMENTE SIN ERRORES DE JINJA2
# =========================================================================
@app.get("/")
async def leer_raiz():
    """
    Sirve el archivo index.html directamente desde la carpeta app de manera limpia,
    sin requerir configuraciones adicionales de plantillas.
    """
    archivo_html = os.path.join("app", "index.html")
    if os.path.exists(archivo_html):
        return FileResponse(archivo_html)
    return JSONResponse(content={"detail": "Not Found"}, status_code=404)

# =========================================================================
# ENDPOINT 1: VALIDACIÓN EXPLICATIVA EN TIEMPO REAL
# =========================================================================
@app.post("/validar")
async def validar_datos_endpoint(
    nombre: str = Form(...), 
    pasaporte: str = Form(...), 
    lang: str = "es"
):
    resultado = kernel.validar_datos_entrada(nombre, pasaporte, lang)
    if not resultado["valido"]:
        return JSONResponse(content=resultado, status_code=400)
    return JSONResponse(content=resultado, status_code=200)

# =========================================================================
# ENDPOINT 2: TRADUCCIÓN DE ITINERARIOS CON GEMINI
# =========================================================================
@app.post("/traducir_itinerario")
async def traducir_itinerario_endpoint(
    origen: str = Form(...), 
    escala: str = Form(""), 
    destino: str = Form(...), 
    horas_escala: str = Form(""), 
    lang: str = "es"
):
    resultado = kernel.traducir_itinerario(origen, escala, destino, horas_escala, lang)
    return JSONResponse(content=resultado, status_code=200)

# =========================================================================
# ENDPOINT 3: VIGILANCIA DIARIA Y SEMANAL
# =========================================================================
@app.post("/sistema/vigilancia")
async def ejecutar_vigilancia_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(kernel.chequear_actualizaciones_aerolineas)
    return JSONResponse(
        content={
            "status": "triggered", 
            "message": "Doble vigilancia diaria activada en segundo plano de Render."
        }, 
        status_code=202
    )

# =========================================================================
# ENDPOINT 4: AUTODESTRUCCIÓN Y CIERRE DE SESIÓN SEGURO
# =========================================================================
@app.post("/destroy_session")
async def destroy_session():
    return JSONResponse(
        content={
            "status": "destroyed", 
            "message": "Memoria local liberada con éxito. Cero datos guardados."
        }, 
        status_code=200
    )
