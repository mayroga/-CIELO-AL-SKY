import os
import requests

class AsesorKernel:
    def __init__(self):
        self.iata_db = {
            "LA HABANA": "HAV", "CUBA": "HAV", "HAVANA": "HAV", "HAV": "HAV",
            "MIAMI": "MIA", "MIAMI FL": "MIA", "MIA": "MIA",
            "BOGOTA": "BOG", "BOGOTA COLOMBIA": "BOG", "BOG": "BOG",
            "CANCUN": "CUN", "CUN": "CUN",
            "MEXICO": "MEX", "CIUDAD DE MEXICO": "MEX", "MEX": "MEX",
            "NUEVA YORK": "JFK", "NEW YORK": "JFK", "JFK": "JFK",
            "PANAMA": "PTY", "PTY": "PTY"
        }
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
        self.session_active = False

        self.frases_render_es = [
            "Buscando vuelos disponibles con calma, ya casi encontramos las mejores opciones.",
            "Conectando de forma segura con los sistemas de aerolíneas, un momento por favor.",
            "Todo marcha de maravilla, cotizando cada ruta y conexión con precisión.",
            "Ya casi terminamos de rastrear los pasajes perfectos para tu viaje."
        ]
        self.frases_render_en = [
            "Searching for available flights calmly, we are almost finding the best options.",
            "Connecting securely with airline systems, just a moment please.",
            "Everything is going wonderfully, quoting each route and connection with precision.",
            "We are almost finished tracking down the perfect tickets for your journey."
        ]

        self.frases_respiracion_es = [
            "Sueltas el control de lo que no puedes cambiar. Inhala despacio... y exhala suave.",
            "Todo está fluyendo de manera correcta. Mantén la calma, ya estamos encontrando tu vuelo.",
            "Respira hondo como un roble fuerte. Cada latido te acerca más a tu destino."
        ]
        self.frases_respiracion_en = [
            "You release control of what you cannot change. Inhale slowly... and exhale softly.",
            "Everything is flowing correctly. Stay calm, we are already finding your flight.",
            "Breathe deeply like a strong tree. Every heartbeat brings you closer to your destination."
        ]

    def obtener_url_aerolinea(self, nombre):
        return self.aerolineas_autorizadas.get(nombre)

    def validar_datos_entrada(self, nombre: str, pasaporte: str, lang: str = "es"):
        try:
            if not nombre or not pasaporte:
                return {"valido": False, "error": "Te falta información. Escribe nombre y pasaporte." if lang == "es" else "Missing info. Please enter name and passport."}
            
            if any(char.isdigit() for char in nombre):
                return {"valido": False, "error": "¡Opa! El nombre solo lleva letras." if lang == "es" else "Oops! Names only contain letters."}
            
            return {"valido": True, "mensaje": "¡Listo!" if lang == "es" else "Ready!"}
        except Exception as e:
            return {"valido": False, "error": "Error de validación interno."}

    def traducir_itinerario(self, origen: str, escala: str, destino: str, horas_escala: str, lang: str = "es"):
        if lang == "es":
            salida = f"Vuelo inicial saliendo desde {origen} con destino al punto de conexión en {escala}."
            estancia = f"Escala confirmada en {escala} con un tiempo de espera de {horas_escala}. Gestión automática de equipaje asegurada."
            llegada = f"Vuelo de conexión desde {escala} con llegada final y directa a {destino}."
            return {"paso_1": salida, "paso_2": estancia, "paso_3": llegada}
        else:
            salida = f"Initial flight departing from {origen} to connection point in {escala}."
            estancia = f"Confirmed layover in {escala} with a wait time of {horas_escala}."
            llegada = f"Connecting flight from {escala} with direct arrival to {destino}."
            return {"paso_1": salida, "paso_2": estancia, "paso_3": llegada}

    def normalizar_lugar(self, texto: str):
        if not texto:
            return None
        return self.iata_db.get(str(texto).upper().strip())

    def obtener_opciones_vuelo(self, origen: str, destino: str, escala: str = "", lang: str = "es"):
        try:
            origen_code = self.normalizar_lugar(origen)
            destino_code = self.normalizar_lugar(destino)

            if not origen_code or not destino_code:
                msg = "No reconozco esa ciudad. Por favor, rectifica el origen o destino para poder asistirte." if lang == "es" else "I don't recognize that city. Please rectify the origin or destination to assist you."
                return {"valido": False, "error": msg}

            token = os.getenv("TRAVELPAYOUTS_API_TOKEN")
            precios_encontrados = []
            
            if token:
                try:
                    url = "https://api.travelpayouts.com/v1/prices/cheap"
                    params = {"origin": origen_code, "destination": destino_code, "token": token, "currency": "USD"}
                    response = requests.get(url, params=params, timeout=5)
                    if response.status_code == 200:
                        data = response.json().get("data", {})
                        if destino_code in data:
                            vuelos_dict = data[destino_code]
                            for k, v in vuelos_dict.items():
                                precios_encontrados.append({
                                    "precio": v.get("price"),
                                    "aerolinea": v.get("airline"),
                                    "enlace": f"https://www.aviasales.com/search/{origen_code}{destino_code}1"
                                })
                            precios_encontrados = sorted(precios_encontrados, key=lambda x: x["precio"])
                except Exception:
                    pass

            if precios_encontrados:
                opciones_dinamicas = []
                for idx, item in enumerate(precios_encontrados[:8], 1):
                    opciones_dinamicas.append({
                        "titulo": f"Opción {idx} - Tarifa: ${item['precio']} USD",
                        "descripcion": f"Aerolínea operadora: {item['aerolinea']}. Ruta hacia {destino} con total respaldo y asesoría."
                    })
                return {
                    "valido": True,
                    "ruta": f"{origen_code} -> {escala + ' -> ' if escala else ''}{destino_code}",
                    "opciones": opciones_dinamicas
                }

            # Respaldo seguro
            if lang == "es":
                return {
                    "valido": True,
                    "ruta": f"{origen_code} -> {escala + ' -> ' if escala else ''}{destino_code}",
                    "opciones": [
                        {"titulo": "1. Opción Económica", "descripcion": f"Vuelo optimizado hacia {destino}."},
                        {"titulo": "2. Opción Protegida", "descripcion": "Respaldo directo con aerolíneas aliadas."},
                        {"titulo": "3. Opción Directa / Especial", "descripcion": f"Búsqueda prioritaria hacia {destino}."},
                        {"titulo": "4. Opción Charter", "descripcion": "Operadores autorizados según disponibilidad."}
                    ]
                }
            else:
                return {
                    "valido": True,
                    "ruta": f"{origen_code} -> {escala + ' -> ' if escala else ''}{destino_code}",
                    "opciones": [
                        {"titulo": "1. Economic Option", "descripcion": f"Optimized flight to {destino}."},
                        {"titulo": "2. Protected Option", "descripcion": "Support with partner airlines."},
                        {"titulo": "3. Direct Option", "descripcion": "Priority search."},
                        {"titulo": "4. Charter Option", "descripcion": "Authorized operators."}
                    ]
                }
        except Exception as e:
            # Esto evita que devuelva 500 en texto plano y congeles el frontend
            return {"valido": False, "error": "Ocurrió un inconveniente procesando la ruta. Por favor, intenta de nuevo." if lang == "es" else "An issue occurred processing the route. Please try again."}
