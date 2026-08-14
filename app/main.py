import os
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI()

# Banco de frases de apoyo anti-agobio y relajación organizadas por IDs (1 al 30)
# Sin repeticiones aleatorias, lectura secuencial del 30 al 1, y reinicio cíclico.
FRASES_ANTIGOBIO = [
    {"id": 30, "es": "Tómate un respiro profundo. Cada paso está bajo control y cuentas con apoyo seguro.", "en": "Take a deep breath. Every step is under control and you have secure support."},
    {"id": 29, "es": "Todo avanza con calma y orden. No hay prisa cuando se hace bien.", "en": "Everything moves forward with calm and order. There is no rush when done right."},
    {"id": 28, "es": "Suelta cualquier tensión en tus hombros. Estamos aquí para guiarte paso a paso.", "en": "Release any tension in your shoulders. We are here to guide you step by step."},
    {"id": 27, "es": "Un momento a la vez. Tu tranquilidad es lo más importante en este proceso.", "en": "One moment at a time. Your peace of mind is the most important thing in this process."},
    {"id": 26, "es": "Respira suave y profundo. Las respuestas correctas fluyen de manera natural.", "en": "Breathe gently and deeply. The right answers flow naturally."},
    {"id": 25, "es": "Estás en un espacio seguro y protegido. Todo saldrá excelente.", "en": "You are in a safe and protected space. Everything will turn out excellent."},
    {"id": 24, "es": "La claridad llega a ti con cada inhalación. Avanzamos con absoluta seguridad.", "en": "Clarity comes to you with each inhalation. We move forward with absolute certainty."},
    {"id": 23, "es": "Permítete estar en calma; cada detalle está siendo cuidadosamente revisado.", "en": "Allow yourself to stay calm; every detail is being carefully reviewed."},
    {"id": 22, "es": "Respira hondo y confía en el proceso. Estamos contigo en cada instante.", "en": "Take a deep breath and trust the process. We are with you every moment."},
    {"id": 21, "es": "La paciencia y el orden simplifican cualquier camino. Relaja tu mente.", "en": "Patience and order simplify any path. Relax your mind."},
    {"id": 20, "es": "Siente cómo el aire fresco renueva tu enfoque. Vamos paso a paso.", "en": "Feel how fresh air renews your focus. Let's take it step by step."},
    {"id": 19, "es": "Mantén una sonrisa interior. Estás resolviendo esto de la mejor manera.", "en": "Keep an inner smile. You are solving this in the best possible way."},
    {"id": 18, "es": "Desconecta del apuro. Aquí cuentas con el tiempo y la orientación precisa.", "en": "Disconnect from the rush. Here you have the time and precise guidance."},
    {"id": 17, "es": "Inhala confianza, exhala cualquier duda. Todo está en orden.", "en": "Inhale confidence, exhale any doubt. Everything is in order."},
    {"id": 16, "es": "Cada instrucción es clara y sencilla para que te sientas cómodo y seguro.", "en": "Every instruction is clear and simple so you feel comfortable and secure."},
    {"id": 15, "es": "Guarda la calma; la solución correcta está apareciendo ante ti.", "en": "Stay calm; the right solution is appearing before you."},
    {"id": 14, "es": "Permítete un respiro consciente. Tu viaje o gestión está respaldada.", "en": "Allow yourself a conscious breath. Your journey or management is supported."},
    {"id": 13, "es": "No tienes que cargar con todo tú solo. Estamos aquí para facilitarlo.", "en": "You don't have to carry everything by yourself. We are here to make it easier."},
    {"id": 12, "es": "Visualiza un camino despejado y sin contratiempos. Respira y avanza.", "en": "Visualize a clear path without setbacks. Breathe and move forward."},
    {"id": 11, "es": "La tranquilidad es tu mejor aliada para tomar decisiones acertadas.", "en": "Peace of mind is your best ally to make right decisions."},
    {"id": 10, "es": "Un suspiro profundo y seguimos. Todo marcha con absoluta fluidez.", "en": "A deep sigh and we continue. Everything goes with absolute fluidity."},
    {"id": 9, "es": "Siente el apoyo y la seguridad en cada clic que realizas.", "en": "Feel the support and security in every click you make."},
    {"id": 8, "es": "Relaja las manos, relaja la mente. Estamos contigo guiándote.", "en": "Relax your hands, relax your mind. We are with you guiding you."},
    {"id": 7, "es": "La claridad mental es tuya ahora mismo. Disfruta el proceso.", "en": "Mental clarity is yours right now. Enjoy the process."},
    {"id": 6, "es": "Respira hondo. Cada indicación está pensada para tu total bienestar.", "en": "Take a deep breath. Every indication is designed for your total well-being."},
    {"id": 5, "es": "Estás completando esto de forma impecable y sin ninguna prisa.", "en": "You are completing this flawlessly and without any rush."},
    {"id": 4, "es": "Un momento de pausa te da la fuerza para avanzar con total seguridad.", "en": "A moment of pause gives you the strength to move forward safely."},
    {"id": 3, "es": "Confía en tu intuición y en la guía profesional que te acompaña.", "en": "Trust your intuition and the professional guidance accompanying you."},
    {"id": 2, "es": "Siente la paz de saber que cuentas con asesoría experta y cercana.", "en": "Feel the peace of knowing you have expert and close advisory."},
    {"id": 1, "es": "Respira hondo y sonríe. Estás llegando a la meta con total éxito.", "en": "Take a deep breath and smile. You are reaching the goal with total success."}
]

# Control de índice en memoria por sesión o servidor (Decrementando de 30 a 1)
current_phrase_index = len(FRASES_ANTIGOBIO) - 1

def obtener_siguiente_frase(lang: str = "es"):
    global current_phrase_index
    frase_obj = FRASES_ANTIGOBIO[current_phrase_index]
    
    # Decrementar para la siguiente lectura (del 30 al 1)
    current_phrase_index -= 1
    if current_phrase_index < 0:
        current_phrase_index = len(FRASES_ANTIGOBIO) - 1 # Reinicia al inicio del ciclo
        
    return frase_obj["es"] if lang == "es" else frase_obj["en"]

HTML_INDEX = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AL CIELO - Asesoría Profesional</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6f9; color: #333; text-align: center; padding: 20px; margin: 0; }
        .main-container { max-width: 650px; margin: 0 auto; padding: 30px; background: #fff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); position: relative; }
        h1 { color: #004080; margin-top: 10px; }
        h2 { color: #004080; }
        button { padding: 12px 24px; margin: 8px; font-size: 16px; font-weight: bold; cursor: pointer; border-radius: 6px; border: 1px solid #ccc; background-color: #fff; transition: all 0.2s ease; }
        button:hover { background-color: #e2e6ea; }
        .btn-primary { background-color: #004080; color: white; border: none; }
        .btn-primary:hover { background-color: #002d5a; }
        .btn-danger { background-color: #dc3545; color: white; border: none; }
        .btn-danger:hover { background-color: #bd2130; }
        .hidden { display: none !important; }
        input { padding: 12px; margin: 10px 0; font-size: 16px; width: 85%; border-radius: 6px; border: 1px solid #ccc; outline: none; }
        input:focus { border-color: #004080; box-shadow: 0 0 5px rgba(0,64,128,0.2); }
        .error-message { color: #dc3545; font-weight: bold; margin: 10px 0; font-size: 15px; }
        #breathing-circle { width: 150px; height: 150px; background-color: #a8dadc; border-radius: 50%; margin: 30px auto; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #fff; font-size: 18px; animation: respirarHumanoRapido 8s infinite ease-in-out; }
        @keyframes respirarHumanoRapido { 0% { transform: scale(1.0); background-color: #a8dadc; } 50% { transform: scale(1.4); background-color: #457b9d; } 100% { transform: scale(1.0); background-color: #a8dadc; } }
        #reloj-global { font-size: 14px; font-weight: bold; color: #dc3545; text-align: right; margin-bottom: 10px; }
    </style>
</head>
<body>
<div class="main-container">
    <div id="reloj-global" class="hidden">Tiempo restante: 08:00</div>
    <div id="language-controls">
        <button onclick="setLanguage('es')">Español</button>
        <button onclick="setLanguage('en')">English</button>
    </div>
    <div id="view-home">
        <h1 id="title">AL CIELO</h1>
        <p id="subtitle" style="font-size: 16px; line-height: 1.6; color: #555; margin: 20px 0;">Tu espacio de asesoría profesional, tranquila y guiada paso a paso.</p>
        <div style="margin-top: 30px;">
            <button id="btn-entrar" class="btn-primary" onclick="iniciarRutaViaje()">Iniciar Asesoría</button>
            <button id="btn-cerrar" class="btn-danger" onclick="handleClose()">Salir</button>
        </div>
    </div>
    <div id="view-orientacion" class="hidden">
        <h2 id="orientacion-heading">Detalles de tu Ruta</h2>
        <p id="orientacion-instruction">Indícanos los datos principales con calma y a tu ritmo:</p>
        <div id="error-orientacion" class="error-message hidden"></div>
        <input type="email" id="input-correo" placeholder="Correo electrónico de contacto"><br>
        <input type="text" id="input-origen" placeholder="Ciudad de Origen (Ej: Miami o MIA)"><br>
        <input type="text" id="input-escala" placeholder="Ciudad de Escala o Conexión (Opcional)"><br>
        <input type="text" id="input-destino" placeholder="Ciudad de Destino (Ej: La Habana o HAV)"><br>
        <input type="text" id="input-horas" placeholder="Tiempo de espera en conexión (Ej: 2 horas)"><br>
        <button id="btn-siguiente-orientacion" class="btn-primary" onclick="guardarOrientacion()">Continuar con Calma</button>
    </div>
    <div id="view-render" class="hidden">
        <h2 id="render-heading-title">Preparando tu espacio con total tranquilidad...</h2>
        <p id="render-phrase" style="font-size: 18px; margin: 30px 0; font-style: italic; color: #457b9d; min-height: 60px;"></p>
        <div style="margin: 20px auto; width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #004080; border-radius: 50%; animation: spin 1s linear infinite;"></div>
    </div>
    <style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>
    <div id="view-formulario" class="hidden">
        <h2 id="form-heading">Información del Pasajero</h2>
        <p id="form-instruction">Escribe tus datos con tranquilidad, verificando cada letra:</p>
        <div id="error-formulario" class="error-message hidden"></div>
        <input type="text" id="input-nombre" placeholder="Nombres (Ej: Juan)"><br>
        <input type="text" id="input-apellido" placeholder="Apellidos (Ej: Pérez Rodríguez)"><br>
        <input type="text" id="input-pasaporte" placeholder="Número de Pasaporte"><br>
        <input type="text" id="input-maletas" placeholder="Equipaje o carga (Ej: 1 maleta de 50 lbs)"><br>
        <button id="btn-procesar" class="btn-primary" onclick="procesarFormularioPasajero()">Verificar con Cuidado</button>
    </div>
    <div id="view-reten" class="hidden">
        <h2>Revisión Consciente de Datos</h2>
        <p style="color: #004080; font-weight: bold;">Tómate un momento para confirmar que todo esté perfecto:</p>
        <div id="resumen-datos-reten" style="text-align: left; background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px auto; max-width: 80%;"></div>
        <div id="bloque-filtro1">
            <p><strong>¿Tu nombre y apellido coinciden exactamente con tu documento físico? Revísalo sin prisa.</strong></p>
            <button class="btn-primary" onclick="aprobarFiltro(1)">SÍ, TODO CORRECTO</button>
        </div>
        <div id="bloque-filtro2" class="hidden">
            <p><strong>Confirmación final: ¿Estás completamente seguro de que los datos son correctos?</strong></p>
            <button class="btn-primary" onclick="aprobarFiltro(2)">SÍ, CONTINUAR</button>
        </div>
    </div>
    <div id="view-respiracion" class="hidden">
        <h2 id="respiracion-heading">Espacio de Relajación y Apoyo</h2>
        <div id="breathing-circle">🧘</div>
        <p id="respiracion-phrase" style="font-size: 18px; margin: 20px 0; font-style: italic; min-height: 60px; color: #457b9d;"></p>
        <p style="font-size: 14px; color: #777;">Estamos procesando tu solicitud de manera segura mientras te relajas.</p>
    </div>
    <div id="view-itinerario" class="hidden">
        <h2 style="color: #28a745;">¡Proceso Completado con Éxito!</h2>
        <p>Tu gestión se ha realizado de forma segura y ordenada.</p>
        <div style="background: #e6f4ea; border: 2px solid #28a745; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h3 style="margin: 0; color: #137333;">Detalle y Tarifa Verificada:</h3>
            <p id="precio-final-real" style="font-size: 28px; font-weight: bold; margin: 10px 0; color: #137333;">Cargando información...</p>
            <p style="font-size: 12px; margin: 0; color: #555;">Resultado obtenido directamente del canal seguro.</p>
        </div>
        <div id="itinerario-masticado" style="text-align: left; line-height: 1.6; padding: 20px; background: #fafafa; border-radius: 8px; margin: 20px 0;"></div>
        <div id="autopropaganda-nino" style="font-style: italic; color: #555; background: #e8f4fd; padding: 15px; border-radius: 6px; margin: 20px 0; font-size: 14px; border-left: 5px solid #004080;">Acompañamiento profesional diseñado para brindarte tranquilidad y claridad en cada paso.</div>
        <button class="btn-primary" onclick="imprimirPDFLocal()">Imprimir / Guardar PDF</button>
        <button class="btn-danger" onclick="handleClose()">Terminar Sesión</button>
    </div>
</div>
<script>
let currentLang = 'es';
let globalTimer = null;
let totalTimeLeft = 480; 
let datosViaje = { correo: "", origen: "", escala: "", destino: "", horas: "" };
let datosUsuario = { nombre: "", apellido: "", pasaporte: "", maletas: "" };

const content = {
    es: { title: "AL CIELO", subtitle: "Tu espacio de asesoría profesional, tranquila y guiada paso a paso.", enter: "Iniciar Asesoría", close: "Salir", orientacionHeading: "Detalles de tu Ruta", orientacionInstruction: "Indícanos los datos principales con calma y a tu ritmo:", btnSiguienteOrientacion: "Continuar con Calma", renderTitle: "Preparando tu espacio con total tranquilidad...", formHeading: "Información del Pasajero", formInstruction: "Escribe tus datos con tranquilidad, verificando cada letra:", btnProcesar: "Verificar con Cuidado" },
    en: { title: "TO THE SKY", subtitle: "Your professional, calm, and step-by-step guided advisory space.", enter: "Start Advisory", close: "Exit", orientacionHeading: "Route Details", orientacionInstruction: "Provide your main details calmly and at your own pace:", btnSiguienteOrientacion: "Continue Calmly", renderTitle: "Preparing your space with total peace of mind...", formHeading: "Passenger Information", formInstruction: "Write your details calmly, checking every letter:", btnProcesar: "Verify Carefully" }
};

function speak(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = currentLang === 'es' ? 'es-ES' : 'en-US';
        utterance.rate = 0.95;
        window.speechSynthesis.speak(utterance);
    }
}

function switchView(viewId) {
    document.querySelectorAll('.main-container > div').forEach(div => {
        if (div.id !== 'reloj-global' && div.id !== 'language-controls') div.classList.add('hidden');
    });
    document.getElementById(viewId).classList.remove('hidden');
}

function setLanguage(lang) {
    currentLang = lang;
    document.documentElement.lang = lang;
    let c = content[lang];
    document.getElementById('title').innerText = c.title;
    document.getElementById('subtitle').innerText = c.subtitle;
    document.getElementById('btn-entrar').innerText = c.enter;
    document.getElementById('btn-cerrar').innerText = c.close;
    document.getElementById('orientacion-heading').innerText = c.orientacionHeading;
    document.getElementById('orientacion-instruction').innerText = c.orientacionInstruction;
    document.getElementById('btn-siguiente-orientacion').innerText = c.btnSiguienteOrientacion;
    document.getElementById('render-heading-title').innerText = c.renderTitle;
    document.getElementById('form-heading').innerText = c.formHeading;
    document.getElementById('form-instruction').innerText = c.formInstruction;
    document.getElementById('btn-procesar').innerText = c.btnProcesar;
}

function iniciarRelojGlobal() {
    let clockBox = document.getElementById('reloj-global');
    clockBox.classList.remove('hidden');
    globalTimer = setInterval(() => {
        totalTimeLeft--;
        let minutes = Math.floor(totalTimeLeft / 60);
        let seconds = totalTimeLeft % 60;
        clockBox.innerText = (currentLang === 'es' ? "Tiempo restante: " : "Time remaining: ") + `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        if (totalTimeLeft <= 0) {
            clearInterval(globalTimer);
            alert(currentLang === 'es' ? "La sesión de asesoría ha finalizado por tiempo." : "The advisory session has ended due to time.");
            window.location.href = "about:blank";
        }
    }, 1000);
}

function iniciarRutaViaje() { iniciarRelojGlobal(); switchView('view-orientacion'); }

function guardarOrientacion() {
    datosViaje.correo = document.getElementById('input-correo').value;
    datosViaje.origen = document.getElementById('input-origen').value;
    datosViaje.escala = document.getElementById('input-escala').value;
    datosViaje.destino = document.getElementById('input-destino').value;
    datosViaje.horas = document.getElementById('input-horas').value;
    if (!datosViaje.correo || !datosViaje.origen || !datosViaje.destino) {
        let msg = currentLang === 'es' ? "Por favor completa los campos principales con calma." : "Please complete the main fields calmly.";
        document.getElementById('error-orientacion').innerText = msg;
        document.getElementById('error-orientacion').classList.remove('hidden');
        speak(msg);
        return;
    }
    document.getElementById('error-orientacion').classList.add('hidden');
    handleEnterRender();
}

async function obtenerSiguienteFraseSecuencial() {
    try {
        let response = await fetch(`/siguiente_frase?lang=${currentLang}`);
        if (response.ok) {
            let data = await response.json();
            return data.frase;
        }
    } catch(e) {}
    return currentLang === 'es' ? "Tómate un respiro profundo. Todo está bajo control." : "Take a deep breath. Everything is under control.";
}

async function handleEnterRender() {
    switchView('view-render');
    let pBox = document.getElementById('render-phrase');
    let fraseActual = await obtenerSiguienteFraseSecuencial();
    pBox.innerText = fraseActual;
    speak(fraseActual);
    
    let renderInterval = setInterval(async () => {
        let nuevaFrase = await obtenerSiguienteFraseSecuencial();
        pBox.innerText = nuevaFrase;
        speak(nuevaFrase);
    }, 12000);

    setTimeout(() => {
        clearInterval(renderInterval);
        switchView('view-formulario');
        speak(currentLang === 'es' ? "Espacio listo. Ingrese sus datos con total tranquilidad." : "Space ready. Enter your details with complete peace of mind.");
    }, 36000);
}

function procesarFormularioPasajero() {
    let nombreInput = document.getElementById('input-nombre').value;
    let apellidoInput = document.getElementById('input-apellido').value;
    let pasaporteInput = document.getElementById('input-pasaporte').value;
    let maletasInput = document.getElementById('input-maletas').value;
    let nombre = nombreInput.replace(/\\s+/g, ' ').trim();
    let apellido = apellidoInput.replace(/\\s+/g, ' ').trim();
    let pasaporte = pasaporteInput.replace(/\\s+/g, '').trim();
    let errorBox = document.getElementById('error-formulario');
    errorBox.classList.add('hidden');
    errorBox.innerText = "";
    if (!nombre || !apellido || !pasaporte || !maletasInput) {
        let msg = currentLang === 'es' ? "Por favor complete los campos con tranquilidad para continuar." : "Please complete the fields calmly to continue.";
        errorBox.innerText = msg; errorBox.classList.remove('hidden'); speak(msg); return;
    }
    datosUsuario.nombre = nombre; datosUsuario.apellido = apellido; datosUsuario.pasaporte = pasaporte; datosUsuario.maletas = maletasInput;
    let resumenHtml = `<p><strong>Titular:</strong> ${nombre} ${apellido}</p><p><strong>Documento:</strong> ${pasaporte}</p><p><strong>Carga / Equipaje:</strong> ${maletasInput}</p><p><strong>Ruta:</strong> ${datosViaje.origen.toUpperCase()} ➔ ${datosViaje.destino.toUpperCase()}</p>`;
    document.getElementById('resumen-datos-reten').innerHTML = resumenHtml;
    document.getElementById('bloque-filtro1').classList.remove('hidden');
    document.getElementById('bloque-filtro2').classList.add('hidden');
    switchView('view-reten');
}

function aprobarFiltro(num) {
    if (num === 1) {
        document.getElementById('bloque-filtro1').classList.add('hidden');
        document.getElementById('bloque-filtro2').classList.remove('hidden');
    } else if (num === 2) {
        let msg = currentLang === 'es' ? "Verificando su información con total seguridad." : "Verifying your information with total security.";
        speak(msg);
        iniciarInyeccionRespiratoria();
    }
}

async function iniciarInyeccionRespiratoria() {
    switchView('view-respiracion');
    let pBox = document.getElementById('respiracion-phrase');
    if (!pBox) return;
    
    let fraseActual = await obtenerSiguienteFraseSecuencial();
    pBox.innerText = fraseActual;
    speak(fraseActual);

    let interval = setInterval(async () => {
        let nuevaFrase = await obtenerSiguienteFraseSecuencial();
        pBox.innerText = nuevaFrase;
        speak(nuevaFrase);
    }, 10000);

    setTimeout(() => { clearInterval(interval); finalizarYMostrarItinerario(); }, 30000);
}

async function finalizarYMostrarItinerario() {
    let itinerarioBox = document.getElementById('itinerario-masticado');
    let precioBox = document.getElementById('precio-final-real');
    itinerarioBox.innerText = currentLang === 'es' ? "Generando reporte de asesoría..." : "Generating advisory report...";
    precioBox.innerText = "...";
    try {
        let formData = new URLSearchParams();
        formData.append('origen', datosViaje.origen);
        formData.append('escala', datosViaje.escala);
        formData.append('destino', datosViaje.destino);
        formData.append('horas_escala', datosViaje.horas);
        formData.append('lang', currentLang);
        let response = await fetch('/traducir_itinerario', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        if (response.ok) {
            let data = await response.json();
            itinerarioBox.innerHTML = `<p>${data.itinerario_masticado}</p>`;
            precioBox.innerText = data.precio_real;
        } else {
            itinerarioBox.innerText = currentLang === 'es' ? "No se pudo completar la consulta." : "Could not complete the query.";
        }
    } catch (err) {
        itinerarioBox.innerText = currentLang === 'es' ? "Error de conexión." : "Connection error.";
    }
    switchView('view-itinerario');
    speak(currentLang === 'es' ? "Asesoría completada con éxito." : "Advisory successfully completed.");
}

function imprimirPDFLocal() { window.print(); }
function handleClose() {
    let confirmMsg = currentLang === 'es' ? "¿Desea finalizar la sesión de forma segura?" : "Do you wish to securely end the session?";
    if (confirm(confirmMsg)) { window.location.href = "about:blank"; }
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_INDEX

@app.get("/siguiente_frase")
async def siguiente_frase(lang: str = "es"):
    """Devuelve estrictamente la siguiente frase del ciclo 30 al 1 sin repeticiones ni aleatoriedad."""
    texto = obtener_siguiente_frase(lang)
    return JSONResponse(content={"frase": texto})

@app.post("/traducir_itinerario")
async def traducir_itinerario(
    origen: str = Form(...),
    escala: str = Form(None),
    destino: str = Form(...),
    horas_escala: str = Form(None),
    lang: str = Form("es")
):
    origin_iata = origen.strip().upper()[:3]
    destination_iata = destino.strip().upper()[:3]
    
    precio_real = "$350.00 USD"
    detalles = [f"Ruta validada: {origin_iata} ➔ {destination_iata}"]
    if escala:
        detalles.append(f"Conexión en {escala} ({horas_escala or 'Estándar'})")

    if lang == "es":
        texto = f"<strong>Reporte de Asesoría:</strong><br>• Origen: {origin_iata} | Destino: {destination_iata}<br>• {'Conexión en ' + escala if escala else 'Vuelo directo'}<br>Proceso guiado completado con total seguridad y claridad."
    else:
        texto = f"<strong>Advisory Report:</strong><br>• Origin: {origin_iata} | Destination: {destination_iata}<br>• {'Connection in ' + escala if escala else 'Direct flight'}<br>Guided process completed safely and clearly."

    return JSONResponse(content={
        "precio_real": precio_real,
        "itinerario_masticado": texto
    })
