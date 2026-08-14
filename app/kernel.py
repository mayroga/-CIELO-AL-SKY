class AsesorKernel:
    def __init__(self):
        # Rango de cobertura cerrado según Plan Maestro
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

    def obtener_url_aerolinea(self, nombre):
        return self.aerolineas_autorizadas.get(nombre)

    def obtener_mensaje(self, clave, lang="es"):
        mensajes = {
            "error_nombre": {
                "es": "¡Opa! Pusiste un número en tu nombre. Solo letras bonitas, quita el número para continuar.",
                "en": "Oops! You put a number in your name. Only beautiful letters, please remove the number to continue."
            },
            "bienvenida": {
                "es": "Bienvenido a AL CIELO",
                "en": "Welcome to AL CIELO"
            }
        }
        return mensajes.get(clave, {}).get(lang, "Error")
