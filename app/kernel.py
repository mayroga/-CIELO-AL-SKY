import os
import requests
import json
from google import genai
from google.genai import types

class AsesorKernel:
    def __init__(self):
        # Base de datos de aeropuertos para normalización rápida
        self.iata_db = {
            "LA HABANA": "HAV", "CUBA": "HAV", "HAVANA": "HAV", "HAV": "HAV",
            "MIAMI": "MIA", "MIAMI FL": "MIA", "MIA": "MIA",
            "BOGOTA": "BOG", "BOGOTA COLOMBIA": "BOG", "BOG": "BOG",
            "CANCUN": "CUN", "CUN": "CUN",
            "MEXICO": "MEX", "CIUDAD DE MEXICO": "MEX", "MEX": "MEX",
            "NUEVA YORK": "JFK", "NEW YORK": "JFK", "JFK": "JFK",
            "PANAMA": "PTY", "PTY": "PTY"
        }
        
        # Rango de cobertura cerrado de aerolíneas aliadas y chárters
        self.aerolineas_autorizadas = {
            "Copa Airlines": "https://www.copaair.com",
            "Avianca": "https://www.avianca.com",
            "American Airlines": "https://www.aa.com",
            "JetBlue": "https://www.jetblue.com",
            "Southwest": "https://www.southwest.com",
            "Delta Air Lines": "https://www.delta.com",
            "Volaris": "https://www.volaris.com",
            "Viva Aerobus": "https://www.vivaaerobus.com",
            "Aeroméxico": "https://www.aeromexico.com",
            "Wingo": "https://www.wingo.com",
            "Cubazul Air Charter": "https://www.cubazulair.com",
            "Xael Charter": "https://www.xaelcharter.com",
            "Aerocuba": "https://www.aerocuba.com"
        }

        # Inicialización del cliente oficial de Gemini utilizando variables de entorno de Render
        # Esto blinda tu API Key frente a robos en repositorios públicos de GitHub
        gemini_key = os.getenv("GEMINI_API_KEY")
        self.ai_client = genai.Client(api_key=gemini_key) if gemini_key else None
        
        # Repositorio volátil de mapas de inyección para automatización
        self.mapas_selectores_locales = {}

        # Frases únicas de carga para el despertar de Render (Completamente distintas a la respiración)
        self.frases_render_es = [
            "Estás haciendo las cosas bien. Tu asistente está despertando los sistemas oficiales.",
            "Asegurando una conexión privada limpia y transparente. Relájate un momento.",
            "Protegiendo tu búsqueda de cambios raros. Tu paciencia vale muchísimo."
        ]
        self.frases_render_en = [
            "You are doing great. Your assistant is waking up the official systems.",
            "Securing a clean and transparent private connection. Relax for a moment.",
            "Protecting your search from unexpected changes. Your patience is highly valued."
        ]

    # =========================================================================
    # RECTIFICACIÓN DE CARACTERES EN TIEMPO REAL (ESTILO NIÑO DE 8 AÑOS)
    # =========================================================================
    def validar_datos_entrada(self, nombre: str, pasaporte: str, lang: str = "es"):
        """
        Bloquea cualquier funcionamiento fantasma. Limpia dobles espacios y valida de
        forma estricta caracteres inválidos, explicando el error como a un niño de 8 años.
        """
        try:
            # Eliminar espacios múltiples internos y laterales
            nombre_limpio = " ".join(nombre.split()).strip()
            pasaporte_limpio = pasaporte.replace(" ", "").strip()

            if not nombre_limpio or not pasaporte_limpio:
                return {
                    "valido": False,
                    "error": "¡Opa! Te saltaste un cuadro vacío. Por favor llénalos todos para que el avión sepa quién eres." if lang == "es" 
                    else "Oops! You skipped a blank box. Please fill them all so the plane knows who you are."
                }

            # Detección de números o símbolos en campos de texto alfabéticos
            if any(char.isdigit() for char in nombre_limpio):
                return {
                    "valido": False,
                    "error": "¡Opa! Pusiste un número dentro de tu nombre o apellido. Los nombres solo llevan letras bonitas, quítalo para continuar." if lang == "es"
                    else "Oops! You put a number inside your name. Names only have pretty letters, remove it to continue."
                }

            return {
                "valido": True, 
                "nombre_depurado": nombre_limpio, 
                "pasaporte_depurado": pasaporte_limpio,
                "mensaje": "¡Listo!" if lang == "es" else "Ready!"
            }
        except Exception:
            return {
                "valido": False, 
                "error": "Ocurrió un inconveniente procesando tus datos. Revisa la pantalla." if lang == "es"
                else "An issue occurred processing your data. Check the screen."
            }

    # =========================================================================
    # TRADUCCIÓN DE ITINERARIO CON IA (ESTILO NIÑO DE 8 AÑOS - CERO PRECIOS INVENTADOS)
    # =========================================================================
    def traducir_itinerario(self, origen: str, escala: str, destino: str, horas_escala: str, lang: str = "es"):
        """
        Llama de forma directa a la API de Gemini para masticar el itinerario técnico
        de los aeropuertos en un lenguaje infantil, directo y libre de agobios o tecnicismos.
        """
        if not self.ai_client:
            # Fallback seguro en caso de que Render no tenga la API Key lista
            return {
                "itinerario_masticado": f"Viaje desde {origen} hacia {destino}. Por favor revisa las pantallas del aeropuerto."
            }

        prompt = f"""
        Actúa como un asistente amigable de viajes para un niño de 8 años.
        Traduce el siguiente itinerario de vuelo a una historia cronológica muy corta y ultra sencilla:
        - Origen: {origen}
        - Escala / Conexión: {escala if escala else 'Ninguna (Vuelo Directo)'}
        - Destino Final: {destino}
        - Tiempo de espera en escala: {horas_escala}
        
        Reglas de escritura obligatorias:
        1. Explica los pasos numerados del 1 al 3 usando palabras dulces como 'Te subes al avión', 'vuelas por los aires', 'esperas caminando tranquilo'.
        2. Explica explícitamente qué pasa con el equipaje: aclara que la aerolínea se encarga de cambiar las maletas grandes de avión por ellos mientras descansan.
        3. Si la escala es corta, advierte amablemente que deben caminar rápido sin distraerse.
        4. Responde estrictamente en idioma: {lang}.
        """

        try:
            response = self.ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return {"itinerario_masticado": response.text.strip()}
        except Exception:
            return {"itinerario_masticado": f"Tu vuelo te llevará desde {origen} hasta {destino} de forma segura."}

    # =========================================================================
    # MOTOR DE DOBLE VIGILANCIA (DIARIA / SEMANAL) Y BORRADO DE OBSOLESCENCIA
    # =========================================================================
    def chequear_actualizaciones_aerolineas(self):
        """
        Simulación del motor de Doble Vigilancia ejecutado de forma interna por el servidor.
        Descarga el HTML público de los formularios chárter/comerciales, Gemini analiza
        los cambios en los campos y SUSTITUYE por completo los datos viejos para optimizar velocidad.
        """
        if not self.ai_client:
            return {"status": "error", "message": "API de Gemini no vinculada en Render."}

        # Simulación de esqueleto HTML capturado del formulario público de Copa Airlines o Cubazul
        html_publico_aerolinea = """
        <form id="passenger-checkout-form">
            <input type="text" name="passenger_first_name_updated" placeholder="First Name">
            <input type="text" name="passenger_passport_id_new" placeholder="Passport Number">
        </form>
        """

        prompt = """
        Analiza este fragmento de código HTML público de formulario de aerolínea y extrae los selectores CSS exactos para los campos: Nombre y Pasaporte.
        Devuelve estrictamente un objeto JSON con las llaves 'selector_nombre' y 'selector_pasaporte'.
        """

        try:
            response = self.ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=html_publico_aerolinea,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            # SUSTITUCIÓN AUTOMÁTICA Y ELIMINACIÓN DE DATOS VIEJOS DE LA MEMORIA
            # Borra por completo el historial antiguo para garantizar espacio libre y rapidez instantánea
            self.mapas_selectores_locales.clear() 
            
            # Carga el nuevo mapa depurado libre de residuos digitales
            self.mapas_selectores_locales = json.loads(response.text)
            return {"status": "success", "message": "Doble vigilancia completada. Sistema limpio de residuos obsoletos."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
