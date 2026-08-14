class AsesorKernel:
    def __init__(self):
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
        if any(char.isdigit() for char in nombre):
            if lang == "es":
                return {"valido": False, "error": "¡Opa! Pusiste un número dentro del cuadro de tu nombre. Los nombres solo llevan letras, quita ese número para continuar."}
            else:
                return {"valido": False, "error": "Oops! You put a number in your name box. Names only have letters, please remove the number to continue."}
        
        if not nombre.strip() or not pasaporte.strip():
            if lang == "es":
                return {"valido": False, "error": "Te saltaste un espacio importante. Por favor escribe tu nombre y pasaporte para continuar."}
            else:
                return {"valido": False, "error": "You missed an important space. Please write your name and passport to continue."}

        if lang == "es":
            return {"valido": True, "mensaje": "¡Listo! Tus datos están correctos."}
        else:
            return {"valido": True, "mensaje": "Ready! Your data is correct."}

    def traducir_itinerario(self, origen: str, escala: str, destino: str, horas_escala: str, lang: str = "es"):
        if lang == "es":
            if escala and escala.strip():
                paso_1 = f"Vuelo inicial saliendo desde {origen} con destino al punto de conexión en {escala}."
                paso_2 = f"Escala confirmada en {escala} con un tiempo de espera de {horas_escala}. Gestión automática de equipaje en tránsito asegurada por la aerolínea."
                paso_3 = f"Vuelo de conexión desde {escala} con llegada final y directa a {destino}."
            else:
                paso_1 = f"Vuelo directo programado y confirmado saliendo desde {origen}."
                paso_2 = ""
                paso_3 = f"Llegada directa y sin escalas al destino final en {destino}."
            return {"paso_1": paso_1, "paso_2": paso_2, "paso_3": paso_3}
        else:
            if escala and escala.strip():
                paso_1 = f"Initial flight departing from {origen} to the connection point in {escala}."
                paso_2 = f"Confirmed layover in {escala} with a wait time of {horas_escala}. Automatic luggage transfer in transit handled by the airline."
                paso_3 = f"Connecting flight from {escala} with final direct arrival to {destino}."
            else:
                paso_1 = f"Scheduled direct flight departing from {origen}."
                paso_2 = ""
                paso_3 = f"Direct arrival with no stops to the final destination in {destino}."
            return {"paso_1": paso_1, "paso_2": paso_2, "paso_3": paso_3}

    def obtener_opciones_vuelo(self, origen: str, destino: str, escala: str = "", lang: str = "es"):
        ruta_str = f"{origen} -> {escala + ' -> ' if escala and escala.strip() else ''}{destino}"
        if lang == "es":
            return {
                "ruta": ruta_str,
                "opciones": [
                    {
                        "titulo": "1. Opción Económica (Conexión / Vuelo Regular)",
                        "descripcion": f"Vuelo optimizado para buscar la tarifa más baja disponible en la ruta {ruta_str}, gestionando tarifas accesibles."
                    },
                    {
                        "titulo": "2. Opción Protegida (Aerolíneas Autorizadas)",
                        "descripcion": f"Incluye cobertura de equipaje y respaldo directo con aerolíneas aliadas para la ruta {ruta_str}."
                    },
                    {
                        "titulo": "3. Opción Directa / Especial",
                        "descripcion": f"Búsqueda prioritaria de vuelos directos o con el menor tiempo de tránsito posible hacia {destino}."
                    },
                    {
                        "titulo": "4. Opción Charter / Alternativa",
                        "descripcion": f"Opciones adicionales a través de operadores autorizados (Cubazul, Xael, Aerocuba) para {destino} según disponibilidad."
                    }
                ]
            }
        else:
            return {
                "ruta": ruta_str,
                "opciones": [
                    {
                        "titulo": "1. Economic Option (Connection / Regular Flight)",
                        "descripcion": f"Optimized flight looking for the lowest available fare on route {ruta_str}, managing affordable rates."
                    },
                    {
                        "titulo": "2. Protected Option (Authorized Airlines)",
                        "descripcion": f"Includes luggage coverage and direct support with partner airlines for route {ruta_str}."
                    },
                    {
                        "titulo": "3. Direct / Special Option",
                        "descripcion": f"Priority search for direct flights or with the shortest transit time to {destino}."
                    },
                    {
                        "titulo": "4. Charter / Alternative Option",
                        "descripcion": f"Additional options through authorized operators for {destino} based on route availability."
                    }
                ]
            }
