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
            "Despertando los motores con calma, ya casi estamos listos para ti.",
            "Conectando de forma segura con el servidor de tu viaje, un momento por favor.",
            "Todo marcha de maravilla, preparando cada detalle con cariño.",
            "Ya casi terminamos de acomodar todo para que tu camino sea perfecto."
        ]
        self.frases_render_en = [
            "Waking up the engines calmly, we are almost ready for you.",
            "Connecting securely to your travel server, just a moment please.",
            "Everything is going wonderfully, preparing every detail with care.",
            "We are almost finished getting everything ready so your journey is perfect."
        ]

        self.frases_respiracion_es = [
            "Sueltas el control de lo que no puedes cambiar. Inhala despacio... y exhala suave.",
            "Todo está fluyendo de manera correcta. Mantén la calma, ya estás muy cerca de casa.",
            "Respira hondo como un roble fuerte. Cada latido te acerca más a los tuyos."
        ]
        self.frases_respiracion_en = [
            "You release control of what you cannot change. Inhale slowly... and exhale softly.",
            "Everything is flowing correctly. Stay calm, you are very close to home.",
            "Breathe deeply like a strong tree. Every heartbeat brings you closer to your loved ones."
        ]

    def obtener_url_aerolinea(self, nombre):
        return self.aerolineas_autorizadas.get(nombre)

    def validar_datos_entrada(self, nombre: str, pasaporte: str, lang: str = "es"):
        if any(char.isdigit() for char in nombre):
            if lang == "es":
                return {"valido": False, "error": "¡Opa! Pusiste un número dentro del cuadro de tu nombre. Los nombres solo llevan letras bonitas, quita ese número para que podamos continuar."}
            else:
                return {"valido": False, "error": "Oops! You put a number in your name box. Names only have beautiful letters, please remove the number so we can continue."}
        
        if not nombre.strip() or not pasaporte.strip():
            if lang == "es":
                return {"valido": False, "error": "Te saltaste un espacio importante. Eso es como la llave de tu puerta, por favor escríbelo para que todo salga perfecto."}
            else:
                return {"valido": False, "error": "You missed an important space. That is like your door key, please write it down so everything comes out perfect."}

        if lang == "es":
            return {"valido": True, "mensaje": "¡Listo! Tus datos están limpios y perfectos."}
        else:
            return {"valido": True, "mensaje": "Ready! Your data is clean and perfect."}

    def traducir_itinerario(self, origen: str, escala: str, destino: str, horas_escala: str, lang: str = "es"):
        if lang == "es":
            salida = f"Te subes al primer avioncito en la linda ciudad de {origen}."
            estancia = f"Este avión aterriza en el aeropuerto de {escala}. Allí te vas a bajar tranquilamente y vas a esperar sentado o caminando un ratito durante {horas_escala}. No tienes que arrastrar tus maletas grandes; la aerolínea las cuida y las cambia de avión por ti mientras descansas."
            llegada = f"Te subes al segundo avión en ese mismo lugar y este te lleva derechito a tu destino final en {destino}. ¡Llegaste a los brazos de los tuyos!"
            return {"paso_1": salida, "paso_2": estancia, "paso_3": llegada}
        else:
            salida = f"You board the first little plane in the lovely city of {origen}."
            estancia = f"This plane lands at the airport in {escala}. There you will get off calmly and wait sitting or walking a little bit for {horas_escala}. You do not have to drag your big suitcases; the airline takes care of them and moves them to your next plane while you rest."
            llegada = f"You board the second plane at that same place and it takes you straight to your final destination in {destino}. You arrived safe and sound!"
            return {"paso_1": salida, "paso_2": estancia, "paso_3": llegada}

    def obtener_opciones_vuelo(self, lang: str = "es"):
        if lang == "es":
            return {
                "opciones": [
                    {
                        "titulo": "1. La Opción Más Barata (Ahorro total)",
                        "descripcion": "Aquí gastas la menor cantidad de dinero posible en tu pasaje. Te lleva a tu destino cuidando cada centavito de tu bolsillo."
                    },
                    {
                        "titulo": "2. La Opción con Seguro (Viaje protegido)",
                        "descripcion": "Pagas un poquito más, pero ya viene con tu seguro médico y de maletas incluido por la aerolínea para que viajes sin ninguna preocupación."
                    },
                    {
                        "titulo": "3. La Opción Especial (Vuelo directo y cómodo)",
                        "descripcion": "Es el viaje directo, sin escalas cansadas, con los horarios más bonitos del día y con tu maleta grande ya lista para volar contigo."
                    },
                    {
                        "titulo": "4. La Opción a Tu Medida (Pedido especial)",
                        "descripcion": "Si quieres algo diferente, me platicas exactamente cómo lo imaginas y buscamos un vuelo hecho a la medida solo para ti."
                    }
                ]
            }
        else:
            return {
                "opciones": [
                    {
                        "titulo": "1. The Cheapest Option (Total savings)",
                        "descripcion": "Here you spend the least possible money on your ticket. It takes you to your destination while taking care of every penny."
                    },
                    {
                        "titulo": "2. The Option with Insurance (Protected trip)",
                        "descripcion": "You pay a little more, but it already includes medical and luggage insurance from the airline so you can travel completely worry-free."
                    },
                    {
                        "titulo": "3. The Special Option (Direct and cozy flight)",
                        "descripcion": "This is the direct trip, without tiring stops, with the nicest times of the day and with your large suitcase ready to fly with you."
                    },
                    {
                        "titulo": "4. Your Custom Option (Special request)",
                        "descripcion": "If you want something different, tell me exactly how you picture it and we will find a flight tailored just for you."
                    }
                ]
            }
