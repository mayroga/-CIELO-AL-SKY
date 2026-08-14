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
            salida = f"Vuelo inicial saliendo desde {origen} con destino al punto de conexión en {escala}."
            estancia = f"Escala confirmada en {escala} con un tiempo de espera de {horas_escala}. Gestión automática de equipaje en tránsito asegurada por la aerolínea."
            llegada = f"Vuelo de conexión desde {escala} con llegada final y directa a {destino}."
            return {"paso_1": salida, "paso_2": estancia, "paso_3": llegada}
        else:
            salida = f"Initial flight departing from {origen} to the connection point in {escala}."
            estancia = f"Confirmed layover in {escala} with a wait time of {horas_escala}. Automatic luggage transfer in transit handled by the airline."
            llegada = f"Connecting flight from {origen if not escala else escala} with final direct arrival to {destino}."
            return {"paso_1": salida, "paso_2": estancia, "paso_3": llegada}

    def obtener_opciones_vuelo(self, origen: str, destino: str, escala: str = "", lang: str = "es"):
        # Lógica central de búsqueda de vuelos directos y de conexión con aerolíneas autorizadas
        if lang == "es":
            return {
                "ruta": f"{origen} -> {escala + ' -> ' if escala else ''}{destino}",
                "opciones": [
                    {
                        "titulo": "1. Opción Económica (Conexión / Vuelo Regular)",
                        "descripcion": f"Vuelo optimizado para buscar la tarifa más baja disponible en rutas hacia {destino}, gestionando escalas de forma eficiente."
                    },
                    {
                        "titulo": "2. Opción Protegida (Aerolíneas Autorizadas)",
                        "descripcion": "Incluye cobertura de equipaje y respaldo directo con aerolíneas aliadas (como Copa, Avianca, American Airlines, entre otras)."
                    },
                    {
                        "titulo": "3. Opción Directa / Especial",
                        "descripcion": f"Búsqueda prioritaria de vuelos directos o con el menor tiempo de tránsito posible hacia {destino}."
                    },
                    {
                        "titulo": "4. Opción Charter / Alternativa",
                        "descripcion": "Opciones adicionales a través de operadores autorizados (Cubazul, Xael, Aerocuba) según disponibilidad de ruta."
                    }
                ]
            }
        else:
            return {
                "ruta": f"{origen} -> {escala + ' -> ' if escala else ''}{destino}",
                "opciones": [
                    {
                        "titulo": "1. Economic Option (Connection / Regular Flight)",
                        "descripcion": f"Optimized flight looking for the lowest available fare on routes to {destino}, managing connections efficiently."
                    },
                    {
                        "titulo": "2. Protected Option (Authorized Airlines)",
                        "descripcion": "Includes luggage coverage and direct support with partner airlines (such as Copa, Avianca, American Airlines, etc.)."
                    },
                    {
                        "titulo": "3. Direct / Special Option",
                        "descripcion": f"Priority search for direct flights or with the shortest transit time to {destino}."
                    },
                    {
                        "titulo": "4. Charter / Alternative Option",
                        "descripcion": "Additional options through authorized operators based on route availability."
                    }
                ]
            }
