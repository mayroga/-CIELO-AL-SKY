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

        # Banco de frases para el despertar de Render (40-50 segundos) - Exclusivas y rotativas
        self.frases_render_es = [
            "Preparando los motores de asistencia de forma segura para ti.",
            "Estableciendo conexión protegida con el servidor de tu viaje.",
            "Todo está fluyendo correctamente, un segundo más por favor.",
            "Cuidando cada detalle técnico para que tu experiencia sea perfecta."
        ]
        self.frases_render_en = [
            "Preparing secure assistance engines for you.",
            "Establishing a protected connection with your travel server.",
            "Everything is flowing correctly, just a second longer please.",
            "Taking care of every technical detail for a seamless experience."
        ]

        # Banco de frases para el Círculo Respiratorio (60 segundos) - Anti-ansiedad y relajación
        self.frases_respiracion_es = [
            "Sueltas el control de lo que no puedes cambiar, estás a un paso de tu destino.",
            "Todo está fluyendo de manera correcta. Mantén la calma, ya casi estamos ahí.",
            "Respira profundo. Cada esfuerzo que haces hoy te acerca más a los tuyos."
        ]
        self.frases_respiracion_en = [
            "You release control of what you cannot change, you are one step away from your destination.",
            "Everything is flowing smoothly. Stay calm, we are almost there.",
            "Breathe deeply. Every effort you make today brings you closer to your loved ones."
        ]

    def obtener_url_aerolinea(self, nombre):
        return self.aerolineas_autorizadas.get(nombre)

    def validar_datos_entrada(self, nombre: str, pasaporte: str, lang: str = "es"):
        import re
        if any(char.isdigit() for char in nombre):
            if lang == "es":
                return {"valido": False, "error": "¡Opa! Pusiste un número dentro del cuadro de tu nombre. Los nombres solo llevan letras bonitas, quita ese número para que podamos continuar."}
            else:
                return {"valido": False, "error": "Oops! You put a number in your name box. Names only have beautiful letters, please remove the number so we can continue."}
        
        if not nombre.strip() or not pasaporte.strip():
            if lang == "es":
                return {"valido": False, "error": "Te saltaste un cuadro importante. Ese dato es como la llave de tu viaje, por favor escríbelo para que todo salga perfecto."}
            else:
                return {"valido": False, "error": "You missed an important box. That data is like the key to your trip, please write it down so everything is perfect."}

        if lang == "es":
            return {"valido": True, "mensaje": "Datos limpios y correctos."}
        else:
            return {"valido": True, "mensaje": "Clean and correct data."}

    def traducir_itinerario(self, origen: str, escala: str, destino: str, horas_escala: str, lang: str = "es"):
        if lang == "es":
            salida = f"Te subes al primer avión en la ciudad de {origen}."
            estancia = f"Este avión aterriza en el aeropuerto de {escala}. Allí te vas a bajar del avión y vas a esperar sentado o caminando tranquilo durante {horas_escala}. Es un tiempo seguro y cómodo para ti. No tienes que buscar tus maletas grandes en este lugar; la aerolínea se encarga de cambiarlas de avión por ti mientras descansas."
            llegada = f"Te subes al segundo avión en ese mismo aeropuerto de escala y este te llevará directo hasta tu destino final en {destino}. ¡Llegaste a salvo!"
            return {"paso_1": salida, "paso_2": estancia, "paso_3": llegada}
        else:
            salida = f"You board the first plane in the city of {origen}."
            estancia = f"This plane lands at the airport in {escala}. There you will get off the plane and wait sitting or walking quietly for {horas_escala}. It is a safe and comfortable time for you. You do not have to look for your large bags in this place; the airline takes care of changing them for you while you rest."
            llegada = f"You board the second plane at that same layover airport and it will take you straight to your final destination in {destino}. You arrived safely!"
            return {"paso_1": salida, "paso_2": estancia, "paso_3": llegada}

    def obtener_opciones_vuelo(self, lang: str = "es"):
        if lang == "es":
            return [
                {
                    "titulo": "1. Opción Económica (El más barato)",
                    "descripcion": "Esta es la opción donde gastas menos dinero en el pasaje. Te lleva a tu destino ahorrando al máximo cada centavo."
                },
                {
                    "titulo": "2. Opción Protegida (Con seguro)",
                    "descripcion": "Este paga un poquito más, pero ya viene con su seguro médico y de maletas incluido por la aerolínea. Así viajas completamente tranquilo por si pasa cualquier imprevisto."
                },
                {
                    "titulo": "3. Opción Cómoda (El Especial)",
                    "descripcion": "Este es el viaje directo, sin escalas cansadas, con los mejores horarios del día y con tu maleta grande ya incluida para que no tengas que pagar nada extra en el aeropuerto."
                },
                {
                    "titulo": "4. Opción a Tu Medida (A pedido especial)",
                    "descripcion": "Si ninguna de las anteriores te convence del todo, me dices exactamente cómo lo quieres y buscamos un vuelo especial solo para ti."
                }
            ]
        else:
            return [
                {
                    "titulo": "1. Economic Option (Cheapest)",
                    "descripcion": "This is the option where you spend the least money on the ticket. It takes you to your destination while saving every penny."
                },
                {
                    "titulo": "2. Protected Option (With Insurance)",
                    "descripcion": "This costs a little more, but it already includes medical and luggage insurance from the airline. This way you travel completely worry-free."
                },
                {
                    "titulo": "3. Comfortable Option (The Special)",
                    "descripcion": "This is the direct trip, without tiring layovers, with the best times of the day and with your large suitcase already included so you don't pay extra."
                },
                {
                    "titulo": "4. Custom Option (Special Request)",
                    "descripcion": "If none of the above completely convinces you, tell me exactly how you want it and we will look for a special flight just for you."
                }
            ]
