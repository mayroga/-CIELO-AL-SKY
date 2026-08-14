import os
import requests

class AsesorKernel:
    def __init__(self):
        self.iata_db = {
            "LA HABANA": "HAV", "CUBA": "HAV", "HAVANA": "HAV", "HAV": "HAV",
            "MIAMI": "MIA", "MIAMI FL": "MIA", "MIA": "MIA",
            "BOGOTA": "BOG", "BOG": "BOG",
            "CANCUN": "CUN", "CUN": "CUN",
            "MEXICO": "MEX", "MEX": "MEX",
            "NUEVA YORK": "JFK", "NEW YORK": "JFK", "JFK": "JFK",
            "PANAMA": "PTY", "PTY": "PTY"
        }
        self.aerolineas_autorizadas = {
            "Copa Airlines": "https://www.copaair.com", "Avianca": "https://www.avianca.com",
            "American Airlines": "https://www.aa.com", "JetBlue": "https://www.jetblue.com",
            "Southwest": "https://www.southwest.com", "Delta Air Lines": "https://www.delta.com",
            "Volaris": "https://www.volaris.com", "Viva Aerobus": "https://www.vivaaerobus.com",
            "Aeroméxico": "https://www.aeromexico.com", "Wingo": "https://www.wingo.com",
            "Cubazul Air Charter": "https://www.cubazulair.com", "Xael Charter": "https://www.xaelcharter.com",
            "Aerocuba": "https://www.aerocuba.com"
        }
        self.session_active = False

    def normalizar_lugar(self, texto: str):
        return self.iata_db.get(texto.upper().strip())

    def obtener_opciones_vuelo(self, origen: str, destino: str, escala: str = "", lang: str = "es"):
        # 1. Normalización Invisible (El cliente no sabe que esto ocurre)
        origen_code = self.normalizar_lugar(origen)
        destino_code = self.normalizar_lugar(destino)

        # 2. Validación de rectificación (Si no existe en la DB, pedimos corrección)
        if not origen_code or not destino_code:
            error_msg = "No reconozco esa ciudad. Por favor, rectifica el origen o destino para poder asistirte." if lang == "es" else "I don't recognize that city. Please rectify the origin or destination to assist you."
            return {"valido": False, "error": error_msg}

        # 3. Consulta a API con códigos IATA normalizados
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
                        for k, v in data[destino_code].items():
                            precios_encontrados.append({
                                "precio": v.get("price"),
                                "aerolinea": v.get("airline"),
                                "enlace": f"https://www.aviasales.com/search/{origen_code}{destino_code}1"
                            })
                        precios_encontrados = sorted(precios_encontrados, key=lambda x: x["precio"])
            except Exception:
                pass

        # 4. Respuesta con datos encontrados o respaldo
        if precios_encontrados:
            opciones = [{"titulo": f"Opción {idx} - Tarifa: ${item['precio']} USD", "descripcion": f"Aerolínea: {item['aerolinea']}. Ruta con respaldo."} for idx, item in enumerate(precios_encontrados[:8], 1)]
            return {"ruta": f"{origen_code} -> {destino_code}", "opciones": opciones}

        # Respaldo (Si la API no tiene datos o falla)
        if lang == "es":
            return {"ruta": f"{origen} -> {destino}", "opciones": [{"titulo": "1. Opción Económica", "descripcion": "Vuelo optimizado hacia " + destino}, {"titulo": "2. Opción Protegida", "descripcion": "Respaldo con aerolíneas aliadas."}, {"titulo": "3. Opción Directa", "descripcion": "Búsqueda prioritaria."}, {"titulo": "4. Opción Charter", "descripcion": "Operadores autorizados."}]}
        else:
            return {"ruta": f"{origen} -> {destino}", "opciones": [{"titulo": "1. Economic Option", "descripcion": "Optimized flight to " + destino}, {"titulo": "2. Protected Option", "descripcion": "Support with partner airlines."}, {"titulo": "3. Direct Option", "descripcion": "Priority search."}, {"titulo": "4. Charter Option", "descripcion": "Authorized operators."}]}
