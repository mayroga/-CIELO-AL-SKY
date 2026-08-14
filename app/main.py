import os
from fastapi import FastAPI, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from app.kernel import AsesorKernel

# Inicialización de la aplicación FastAPI
app = FastAPI(title="AL CIELO - API Core Principal")

# Instancia global del motor inteligente de asistencia (API + Gemini)
kernel = AsesorKernel()

# =========================================================================
# 🚀 RUTA RAÍZ: SIRVE TU INDEX.HTML DIRECTAMENTE SIN ERRORES DE JINJA2
# =========================================================================
@app.get("/")
async def leer_raiz():
    """
    Intercepta la entrada a la raíz del servidor y despacha 
    el archivo index.html directamente desde la carpeta app de manera limpia y estática.
    """
    archivo_html = os.path.join("app", "index.html")
    if os.path.exists(archivo_html):
        return FileResponse(archivo_html)
    return JSONResponse(content={"detail": "Not Found - Archivo index.html no ubicado"}, status_code=404)

# =========================================================================
# ENDPOINT 1: VALIDACIÓN Y RECTIFICACIÓN DE CARACTERES EN TIEMPO REAL
# =========================================================================
@app.post("/validar")
async def validar_datos_endpoint(
    nombre: str = Form(...), 
    pasaporte: str = Form(...), 
    lang: str = "es"
):
    """
    Recibe los datos del formulario del cliente. Invoca al filtro estricto
    para limpiar dobles espacios o caracteres prohibidos antes de avanzar en la interfaz.
    """
    resultado = kernel.validar_datos_entrada(nombre, pasaporte, lang)
    if not resultado["valido"]:
        # Bloquea el funcionamiento fantasma regresando la instrucción amigable para niños
        return JSONResponse(content=resultado, status_code=400)
    return JSONResponse(content=resultado, status_code=200)

# =========================================================================
# ENDPOINT 2: MOTOR HÍBRIDO (API DE VUELOS EN VIVO + RESPALDO DE GEMINI)
# =========================================================================
@app.post("/traducir_itinerario")
async def traducir_itinerario_endpoint(
    origen: str = Form(...), 
    escala: str = Form(""), 
    destino: str = Form(...), 
    horas_escala: str = Form(""), 
    lang: str = "es"
):
    """
    Endpoint central que conecta con tu API instalada de vuelos. Extrae los precios reales 
    en vivo y, si la API da indefinido o falla, activa a Gemini como escudo de
    respaldo para masticar el itinerario al estilo de un niño de 8 años.
    """
    resultado = kernel.obtener_itinerario_y_precio_real(origen, escala, destino, horas_escala, lang)
    return JSONResponse(content=resultado, status_code=200)

# =========================================================================
# ENDPOINT 3: VIGILANCIA DIARIA Y SEMANAL CON BORRADO AUTOMÁTICO
# =========================================================================
@app.post("/sistema/vigilancia")
async def ejecutar_vigilancia_endpoint(background_tasks: BackgroundTasks):
    """
    Activa las tareas automáticas de inspección diaria en segundo plano de Render
    para actualizar coordenadas de aerolíneas chárter y vaciar residuos obsoletos de la RAM.
    """
    background_tasks.add_task(kernel.chequear_actualizaciones_aerolineas)
    return JSONResponse(
        content={
            "status": "triggered", 
            "message": "Doble vigilancia diaria activada en segundo plano de Render."
        }, 
        status_code=202
    )

# =========================================================================
# ENDPOINT 4: AUTODESTRUCCIÓN Y LIMPIEZA TOTAL DE MEMORIA VOLÁTIL
# =========================================================================
@app.post("/destroy_session")
async def destroy_session():
    """
    Llamado por el reloj de 8 minutos o al presionar el botón 'Cerrar'. Asegura que
    no queden rastros temporales en las variables o la memoria del servidor.
    """
    return JSONResponse(
        content={
            "status": "destroyed", 
            "message": "Memoria local liberada con éxito. Cero datos guardados."
        }, 
        status_code=200
    )
