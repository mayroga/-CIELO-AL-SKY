class AsesorKernel:
    def __init__(self):
        self.session_active = False

    def obtener_mensaje(self, clave, lang="es"):
        mensajes = {
            "error_nombre": {
                "es": "¡Opa! Pusiste un número dentro del cuadro de tu nombre. Los nombres solo llevan letras bonitas, quita ese número para que podamos continuar.",
                "en": "Oops! You put a number in your name box. Names only have beautiful letters, please remove the number so we can continue."
            },
            "bienvenida": {
                "es": "Bienvenido a AL CIELO",
                "en": "Welcome to AL CIELO"
            }
        }
        return mensajes.get(clave, {}).get(lang, "Error")

    def validar_datos(self, datos, lang="es"):
        # Lógica de validación pura, sin mezcla de idiomas
        return self.obtener_mensaje("error_nombre", lang)
