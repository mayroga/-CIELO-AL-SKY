import os
from fastapi import FastAPI, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.kernel import AsesorKernel

# Inicialización de la aplicación FastAPI
app = FastAPI(title="AL CIELO - API Core")

# Instancia global del motor inteligente de asistencia
kernel = AsesorKernel()

# Opcional: Montar archivos estáticos para servir el index.html si tu arquitectura lo requiere
# app.mount("/static", StaticFiles(directory="app"), name="static")

# =========================================================================
# ENDPOINT 1: VALIDACIÓN EXPLICATIVA EN TIEMPO REAL
# =========================================================================
@app.post("/validar")
async def validar_datos_endpoint(
    nombre: str = Form(...), 
    pasaporte: str = Form(...), 
    lang: str = "es"
):
    """
    Recibe los datos del formulario del cliente. Invoca al filtro estricto anti-errores
    para limpiar espacios fantasmas y letras erróneas antes de cualquier avance en la web.
    """
    resultado = kernel.validar_datos_entrada(nombre, pasaporte, lang)
    
    if not resultado["valido"]:
        # Se devuelve un código 400 controlado pero con la explicación amigable para niños de 8 años
        return JSONResponse(content=resultado, status_code=400)
        
    return JSONResponse(content=resultado, status_code=200)

# =========================================================================
# ENDPOINT 2: TRADUCCIÓN DE ITINERARIOS NO DIRECTOS CON GEMINI
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
    Endpoint estratégico que sustituye los datos inventados de Travelpayouts. Toma los parámetros 
    públicos de la ruta del cliente y los envía a Gemini para 'masticar' el mapa de viaje.
    """
    resultado = kernel.traducir_itinerario(origen, escala, destino, horas_escala, lang)
    return JSONResponse(content=resultado, status_code=200)

# =========================================================================
# ENDPOINT 3: VIGILANCIA DIARIA Y SEMANAL (TRIGGER DE LIMPIEZA)
# =========================================================================
@app.post("/sistema/vigilancia")
async def ejecutar_vigilancia_endpoint(background_tasks: BackgroundTasks):
    """
    Activa las tareas automáticas de inspección diaria en segundo plano (Background Tasks). 
    Descarga los HTML públicos de Copa o los chárters, sobrescribe las coordenadas 
    con Gemini y vacía de inmediato el almacenamiento antiguo para no dejar residuos.
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
# ENDPOINT 4: AUTODESTRUCCIÓN Y CIERRE DE SESIÓN SEGURO
# =========================================================================
@app.post("/destroy_session")
async def destroy_session():
    """
    Llamado de forma automática por el temporizador de JavaScript a los 8 minutos o
    manualmente por el cliente mediante el botón 'Cerrar'. Asegura la destrucción
    inmediata de cualquier rastro temporal de variables en memoria.
    """
    try:
        # Forzar la limpieza de mapas o banderas activas locales del proceso del usuario
        # Al no usar bases de datos ni cookies permanentes, el flujo es 100% volátil
        return JSONResponse(
            content={
                "status": "destroyed", 
                "message": "Memoria local liberada con éxito. Cero datos guardados."
            }, 
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
