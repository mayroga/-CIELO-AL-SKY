import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI()

HTML_INDEX = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AL CIELO - Asistente de Viaje Profesional</title>
    <style>
        body, html {
            margin: 0; padding: 0; height: 100%;
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #f4f6f9; color: #333;
        }
        .main-container {
            max-width: 650px;
            margin: 40px auto;
            padding: 30px;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            position: relative;
        }
        h1 { color: #004080; margin-top: 10px; }
        h2 { color: #004080; }
        button {
            padding: 12px 24px;
            margin: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 6px;
            border: 1px solid #ccc;
            background-color: #fff;
            transition: all 0.2s ease;
        }
        button:hover { background-color: #e2e6ea; }
        .btn-primary { background-color: #004080; color: white; border: none; }
        .btn-primary:hover { background-color: #002d5a; }
        .btn-danger { background-color: #dc3545; color: white; border: none; }
        .btn-danger:hover { background-color: #bd2130; }
        .btn-success { background-color: #28a745; color: white; border: none; font-size: 18px; padding: 15px 30px; box-shadow: 0 4px 10px rgba(40,167,69,0.3); }
        .btn-success:hover { background-color: #218838; }
        .hidden { display: none !important; }
        input {
            padding: 12px;
            margin: 10px 0;
            font-size: 16px;
            width: 85%;
            border-radius: 6px;
            border: 1px solid #ccc;
            outline: none;
        }
        input:focus { border-color: #004080; box-shadow: 0 0 5px rgba(0,64,128,0.2); }
        .error-message {
            color: #dc3545;
            font-weight: bold;
            margin: 10px 0;
            font-size: 15px;
        }
        #breathing-circle {
            width: 170px;
            height: 170px;
            background-color: #a8dadc;
            border-radius: 50%;
            margin: 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 15px;
            font-weight: bold;
            color: #fff;
            font-size: 14px;
            box-sizing: border-box;
            animation: respirarHumanoRapido 8s infinite ease-in-out;
        }
        @keyframes respirarHumanoRapido {
            0% { transform: scale(1.0); background-color: #a8dadc; }
            50% { transform: scale(1.35); background-color: #457b9d; }
            100% { transform: scale(1.0); background-color: #a8dadc; }
        }
        
        /* CONSOLA DE ACOMPAÑAMIENTO */
        .app-companion-wrapper {
            max-width: 550px; margin: 30px auto; background: #fff;
            border-radius: 14px; box-shadow: 0 6px 20px rgba(0,0,0,0.1);
            display: flex; flex-direction: column; overflow: hidden; height: 85vh;
        }
        .guardian-header {
            background: #004080; color: white; padding: 18px; text-align: center;
            font-weight: bold; font-size: 20px;
        }
        .guardian-body {
            flex: 1; padding: 20px; overflow-y: auto; text-align: left; font-size: 15px; background: #f8f9fa;
        }
        .chat-bubble {
            background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04); line-height: 1.5; border-left: 5px solid #004080;
        }
        .guardian-footer {
            padding: 15px; background: #fff; border-top: 1px solid #e9ecef;
            display: flex; flex-direction: column; gap: 12px;
        }
        .control-row { display: flex; gap: 10px; align-items: center; }
        .btn-mic { background: #28a745; color: white; flex: 1; }
        .btn-mic.muted { background: #dc3545; }
        .btn-send { background: #004080; color: white; }
    </style>
</head>
<body>
<div id="wrapper-setup-views">
    <div class="main-container">
        <div id="language-controls">
            <button onclick="setLanguage('es')">Español</button>
            <button onclick="setLanguage('en')">English</button>
        </div>

        <!-- VISTA 1: MURO LEGAL -->
        <div id="view-home">
            <h1 id="title">AL CIELO</h1>
            <p id="subtitle" style="font-size: 15px; line-height: 1.6; color: #444; margin: 15px 0; font-weight: bold;">
                Mecanismo Tecnológico Privado de Asistencia y Acompañamiento al Viajero.
            </p>
            
            <div style="text-align: left; background: #f8f9fa; border: 1px solid #ccc; padding: 15px; border-radius: 8px; max-height: 180px; overflow-y: auto; font-size: 13px; line-height: 1.5; margin: 20px 0; border-left: 5px solid #004080;">
                <p><strong>CONTRATO DE MANDATO TÉCNICO Y DECLARACIÓN DE DERECHOS:</strong></p>
                <p>Al presionar 'Acepto y Entrar', usted manifiesta, declara y firma voluntariamente lo siguiente:</p>
                <p>1. Solicito y autorizo de forma expresa a esta aplicación para actuar como mi asistente técnico personal, copiloto informático y guía de acompañamiento en mi pantalla durante mi proceso de consulta en la plataforma pública de Google Flights.</p>
                <p>2. Manifiesto que el uso de esta herramienta responde a mi derecho legítimo de recibir asistencia contra el agobio, el estrés y el cansancio mental derivados de la gestión de viajes.</p>
                <p>3. Comprendo que esta aplicación es un agente informático pasivo y volátil: no almacena mis datos personales ni procesa mis pagos. La decisión final de compra se realiza bajo mi control directo en la ventana oficial externa.</p>
            </div>

            <div style="margin: 15px 0; font-size: 14px; font-weight: bold;">
                <input type="checkbox" id="chk-legal-accept" style="width: auto; margin-right: 10px;" onclick="evaluarAceptacionLegal()">
                <label for="chk-legal-accept" style="cursor:pointer;">He leído, acepto el mandato y firmo este escudo de protección</label>
            </div>

            <div style="margin-top: 20px;">
                <button id="btn-entrar" class="btn-primary" onclick="iniciarRutaViaje()" disabled style="opacity: 0.5; cursor: not-allowed;">Acepto y Entrar</button>
                <button id="btn-cerrar" class="btn-danger" onclick="handleClose()">Cerrar App</button>
            </div>
        </div>

        <!-- VISTA 2: FORMULARIO DE RUTA -->
        <div id="view-form" class="hidden">
            <h2 id="form-title">Datos del Itinerario y Pasajero</h2>
            <p id="form-desc" style="color: #666; font-size: 14px;">Complete los campos para el despliegue de opciones en el motor de Google Fly.</p>
            <div style="margin: 20px 0; text-align: left; display: inline-block; width: 100%;">
                <label style="font-size: 13px; font-weight: bold; color: #004080;" id="lbl-origen">Ciudad de Origen (Código IATA):</label><br>
                <input type="text" id="origen" placeholder="Ej: MIA"><br>
                
                <label style="font-size: 13px; font-weight: bold; color: #004080; margin-top: 10px; display: inline-block;" id="lbl-escala">Escala intermedia opcional:</label><br>
                <input type="text" id="escala" placeholder="Ej: PTY u otro punto"><br>
                
                <label style="font-size: 13px; font-weight: bold; color: #004080; margin-top: 10px; display: inline-block;" id="lbl-destino">Ciudad de Destino (Código IATA):</label><br>
                <input type="text" id="destino" placeholder="Ej: HAV"><br>

                <label style="font-size: 13px; font-weight: bold; color: #004080; margin-top: 10px; display: inline-block;" id="lbl-horas">Tiempo estimado de conexión:</label><br>
                <input type="text" id="horas_escala" placeholder="Ej: 2 horas y media"><br>
            </div>
            <div id="error-box" class="error-message hidden"></div>
            <div style="margin-top: 25px;">
                <button class="btn-primary" id="btn-procesar" onclick="procesarAsesoria()">Verificar y Activar Copiloto</button>
                <button class="btn-danger" id="btn-cancelar" onclick="switchView('view-home')">Cancelar</button>
            </div>
        </div>

        <!-- VISTA 3: CÍRCULO RESPIRATORIO + BOTÓN MANUAL DE GOOGLE FLY ABAJO -->
        <div id="view-loading" class="hidden">
            <h2 id="load-title">Preparando tu Conexión con Google Fly</h2>
            <p id="load-desc" style="color: #666; font-size: 14px;">Inhalando calma, liberando el estrés de ruta...</p>
            
            <!-- Círculo respiratorio con frases secuenciales únicas guardadas en LocalStorage (Kernel Kernel-ready) -->
            <div id="breathing-circle"><span id="breath-txt">Inhala profundo</span></div>
            
            <p id="load-sub" style="font-size: 13px; color: #888; margin-top: 10px;">Tu mente en paz. Cuando estés listo, haz clic en el botón de abajo para activar tu conexión con Google Fly.</p>
            
            <!-- Botón manual obligatorio para conectar con Google Fly ubicado justamente debajo del círculo -->
            <div style="margin-top: 25px;">
                <button class="btn-success" id="btn-conectar-google-fly" onclick="conectarGoogleFlyManual()">✈️ CONECTAR CON GOOGLE FLY</button>
            </div>
        </div>
    </div>
</div>

<!-- CONSOLA FLOTANTE DE ACOMPAÑAMIENTO CON MICRÓFONO Y CHAT -->
<div id="view-split" class="app-companion-wrapper hidden">
    <div class="guardian-header">Copiloto Protector 24/7</div>
    <div class="guardian-body" id="chat-stream">
        <div class="chat-bubble">¡Hola! Estoy aquí contigo. Se ha abierto tu ventana de Google Fly. Puedes hablarme o escribirme aquí si tienes dudas sobre campos de pago, maletas o seguros. Todo saldrá bien.</div>
    </div>
    <div class="guardian-footer">
        <div class="control-row">
            <button id="btn-mic-toggle" class="btn-mic" onclick="toggleMic()">🎙️ Micrófono ON</button>
            <span id="mic-status" style="font-size:12px; color:#555;">Escuchando...</span>
        </div>
        <div class="control-row">
            <input type="text" id="user-input-text" placeholder="Escribe tu duda aquí..." onkeypress="handleKey(event)">
            <button class="btn-send" onclick="enviarTextoDuda()">Enviar</button>
        </div>
        <div class="control-row" style="justify-content: center; margin-top: 5px;">
            <button class="btn-danger" onclick="handleClose()" style="font-size: 12px; padding: 6px 12px; margin: 0;">Terminar Sesión</button>
        </div>
    </div>
</div>

<script>
let currentLang = 'es';
let micActive = true;
let recognition = null;
let urlGoogleFlightsGlobal = "https://www.google.com/travel/flights";
let breathInterval = null;

// Banco estricto y ordenado de frases antiagobio, antiestrés y relajación (sin repetición, orden numérico perfecto)
const frasesRelajacionES = [
    "1. Inhala despacio y suelta cualquier carga mental que lleves.",
    "2. Cada respiración te devuelve la paz y el control total.",
    "3. No hay prisa; tu camino está seguro y protegido hoy.",
    "4. Suelta la tensión de tus hombros; todo está saliendo bien.",
    "5. Respira hondo y confía en el proceso de tu viaje.",
    "6. La tranquilidad es tu mayor aliada en este momento.",
    "7. Un paso a la vez, tu mente se aclara y descansa.",
    "8. Libera el agobio; mereces un viaje tranquilo y sin estrés.",
    "9. Siente el aire puro llenando de calma tu interior.",
    "10. Estás exactamente donde debes estar, seguro y en paz."
];

const frasesRelajacionEN = [
    "1. Inhale slowly and release any heavy mental burden.",
    "2. Each breath brings back your peace and absolute control.",
    "3. There is no rush; your journey is safe and protected.",
    "4. Release tension from your shoulders; everything is fine.",
    "5. Take a deep breath and trust your travel process.",
    "6. Tranquility is your greatest ally at this very moment.",
    "7. One step at a time, your mind clears and rests.",
    "8. Let go of overwhelm; you deserve a calm, stress-free trip.",
    "9. Feel pure air filling your inner self with deep calm.",
    "10. You are right where you need to be, safe and peaceful."
];

// Lógica de Kernel LocalStorage para índice secuencial sin repetición ni reinicios erróneos
function obtenerSiguienteFraseSecuencial() {
    let storageKey = "kernel_breath_index_" + currentLang;
    let indexStr = localStorage.getItem(storageKey);
    let currentIndex = indexStr ? parseInt(indexStr, 10) : 0;
    
    let banco = currentLang === 'es' ? frasesRelajacionES : frasesRelajacionEN;
    
    // Seguridad ante límites
    if (isNaN(currentIndex) || currentIndex < 0 || currentIndex >= banco.length) {
        currentIndex = 0;
    }
    
    let fraseSeleccionada = banco[currentIndex];
    
    // Incrementar y dar la vuelta de manera estricta al terminar el último (bucle cíclico perfecto)
    let siguienteIndex = (currentIndex + 1) % banco.length;
    localStorage.setItem(storageKey, siguienteIndex.toString());
    
    return fraseSeleccionada;
}

function iniciarCicloRespiratorioDinamico() {
    if (breathInterval) clearInterval(breathInterval);
    
    let spanTxt = document.getElementById('breath-txt');
    
    // Mostrar frase inmediata
    let fraseActual = obtenerSiguienteFraseSecuencial();
    spanTxt.innerText = fraseActual;
    speak(fraseActual);
    
    // Rotar automáticamente cada 9 segundos mientras el usuario permanece en la pantalla de carga
    breathInterval = setInterval(() => {
        let proximaFrase = obtenerSiguienteFraseSecuencial();
        spanTxt.innerText = proximaFrase;
        speak(proximaFrase);
    }, 9000);
}

const translations = {
    es: {
        title: "AL CIELO",
        subtitle: "Mecanismo Tecnológico Privado de Asistencia y Acompañamiento al Viajero.",
        entrar: "Acepto y Entrar",
        cerrar: "Cerrar App",
        formTitle: "Datos del Itinerario y Pasajero",
        formDesc: "Complete los campos para el despliegue de opciones en el motor de Google Fly.",
        lblOrigen: "Ciudad de Origen (Código IATA):",
        lblEscala: "Escala intermedia opcional:",
        lblDestino: "Ciudad de Destino (Código IATA):",
        lblHoras: "Tiempo estimado de conexión:",
        procesar: "Verificar y Activar Copiloto",
        cancelar: "Cancelar",
        loadTitle: "Preparando tu Conexión con Google Fly",
        loadDesc: "Inhalando calma, liberando el estrés de ruta..."
    },
    en: {
        title: "TO THE SKY",
        subtitle: "Private Technological Mechanism for Traveler Assistance and Guidance.",
        entrar: "Accept & Enter",
        cerrar: "Close App",
        formTitle: "Itinerary & Passenger Data",
        formDesc: "Fill in the fields to deploy live flight options via Google Fly.",
        lblOrigen: "Origin City (IATA Code):",
        lblEscala: "Optional intermediate stop:",
        lblDestino: "Destination City (IATA Code):",
        lblHoras: "Estimated connection time:",
        procesar: "Verify & Activate Copilot",
        cancelar: "Cancel",
        loadTitle: "Preparing your Connection to Google Fly",
        loadDesc: "Inhaling calm, releasing route stress..."
    }
};

function setLanguage(lang) {
    currentLang = lang;
    let t = translations[lang];
    document.getElementById('title').innerText = t.title;
    document.getElementById('subtitle').innerText = t.subtitle;
    document.getElementById('btn-entrar').innerText = t.entrar;
    document.getElementById('btn-cerrar').innerText = t.cerrar;
    document.getElementById('form-title').innerText = t.formTitle;
    document.getElementById('form-desc').innerText = t.formDesc;
    document.getElementById('lbl-origen').innerText = t.lblOrigen;
    document.getElementById('lbl-escala').innerText = t.lblEscala;
    document.getElementById('lbl-destino').innerText = t.lblDestino;
    document.getElementById('lbl-horas').innerText = t.lblHoras;
    document.getElementById('btn-procesar').innerText = t.procesar;
    document.getElementById('btn-cancelar').innerText = t.cancelar;
    document.getElementById('load-title').innerText = t.loadTitle;
    document.getElementById('load-desc').innerText = t.loadDesc;
}

function switchView(viewId) {
    if (viewId !== 'view-loading' && breathInterval) {
        clearInterval(breathInterval);
        breathInterval = null;
    }
    document.getElementById('view-home').classList.add('hidden');
    document.getElementById('view-form').classList.add('hidden');
    document.getElementById('view-loading').classList.add('hidden');
    document.getElementById('view-split').classList.add('hidden');
    
    if (viewId === 'view-split') {
        document.getElementById('wrapper-setup-views').classList.add('hidden');
    } else {
        document.getElementById('wrapper-setup-views').classList.remove('hidden');
    }
    document.getElementById(viewId).classList.remove('hidden');
}

function evaluarAceptacionLegal() {
    let checkbox = document.getElementById('chk-legal-accept');
    let btnEntrar = document.getElementById('btn-entrar');
    if (checkbox.checked) {
        btnEntrar.disabled = false;
        btnEntrar.style.opacity = "1";
        btnEntrar.style.cursor = "pointer";
    } else {
        btnEntrar.disabled = true;
        btnEntrar.style.opacity = "0.5";
        btnEntrar.style.cursor = "not-allowed";
    }
}

function iniciarRutaViaje() {
    switchView('view-form');
    speak(currentLang === 'es' ? "Por favor ingrese su ciudad de origen y destino." : "Please enter your origin and destination city.");
}

function speak(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        let textoLimpio = text.replace(/<\/?[^>]+(>|$)/g, "").replace(/•/g, "").replace(/➔/g, "hacia").replace(/^\d+\.\s*/, "");
        let utterance = new SpeechSynthesisUtterance(textoLimpio);
        utterance.lang = currentLang === 'es' ? 'es-ES' : 'en-US';
        utterance.rate = 0.95; // Velocidad pausada y relajante
        window.speechSynthesis.speak(utterance);
    }
}

async function procesarAsesoria() {
    let org = document.getElementById('origen').value.trim();
    let dest = document.getElementById('destino').value.trim();
    let esc = document.getElementById('escala').value.trim();
    let hrs = document.getElementById('horas_escala').value.trim();
    let errBox = document.getElementById('error-box');

    if (!org || !dest) {
        let msg = currentLang === 'es' ? "¡Opa! Origen y destino son necesarios." : "Oops! Origin and destination are required.";
        errBox.innerText = msg;
        errBox.classList.remove('hidden');
        speak(msg);
        return;
    }
    errBox.classList.add('hidden');
    
    // Generar URL personalizada con los códigos IATA ingresados por el cliente
    let origin_iata = org.toUpperCase().substring(0, 3);
    let destination_iata = dest.toUpperCase().substring(0, 3);
    urlGoogleFlightsGlobal = `https://www.google.com/travel/flights?q=flights%20from%20${origin_iata}%20to%20${destination_iata}`;

    // Cambiar a la vista del círculo respiratorio
    switchView('view-loading');
    
    // Iniciar el motor de frases antiagobio no repetitivas sincronizadas con LocalStorage
    iniciarCicloRespiratorioDinamico();
} 

// CONEXIÓN MANUAL ESTRICTA: Solo ocurre si el usuario da clic físico en el botón debajo del círculo
function conectarGoogleFlyManual() {
    if (breathInterval) {
        clearInterval(breathInterval);
        breathInterval = null;
    }
    
    // Transición a la consola flotante protectora
    switchView('view-split');
    
    // Abrir ventana oficial con el link oficial de Google Fly
    window.open(urlGoogleFlightsGlobal, '_blank');
    
    // Activar escucha continua de voz y chat asistente
    iniciarReconocimientoVoz();
}

function iniciarReconocimientoVoz() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        document.getElementById('mic-status').innerText = "Voz no soportada.";
        return;
    }
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRec();
    recognition.lang = currentLang === 'es' ? 'es-ES' : 'en-US';
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
        if (!micActive) return;
        let textoDicho = event.results[event.resultIndex][0].transcript;
        agregarMensajeChat(currentLang === 'es' ? "Tú (voz): " + textoDicho : "You (voice): " + textoDicho);
        procesarRespuestaAsistente(textoDicho);
    };

    recognition.onend = () => {
        if (micActive) {
            try { recognition.start(); } catch(e) {}
        }
    };
    try { recognition.start(); } catch(e) {}
}

function toggleMic() {
    micActive = !micActive;
    let btn = document.getElementById('btn-mic-toggle');
    let status = document.getElementById('mic-status');
    if (micActive) {
        btn.innerText = currentLang === 'es' ? "🎙️ Micrófono ON" : "🎙️ Mic Muted OFF";
        btn.classList.remove('muted');
        status.innerText = currentLang === 'es' ? "Escuchando..." : "Listening...";
        if(recognition) try { recognition.start(); } catch(e) {}
        speak(currentLang === 'es' ? "Micrófono encendido." : "Microphone on.");
    } else {
        btn.innerText = currentLang === 'es' ? "🔇 Micrófono OFF" : "🔇 Mic Muted ON";
        btn.classList.add('muted');
        status.innerText = currentLang === 'es' ? "Silenciado." : "Muted.";
        if(recognition) recognition.stop();
        speak(currentLang === 'es' ? "Micrófono apagado." : "Microphone off.");
    }
}

function handleKey(e) {
    if (e.key === 'Enter') enviarTextoDuda();
}

function enviarTextoDuda() {
    let box = document.getElementById('user-input-text');
    let val = box.value.trim();
    if (!val) return;
    agregarMensajeChat(currentLang === 'es' ? "Tú (escrito): " + val : "You (typed): " + val);
    box.value = "";
    procesarRespuestaAsistente(val);
}

function agregarMensajeChat(txt) {
    let stream = document.getElementById('chat-stream');
    let div = document.createElement('div');
    div.className = 'chat-bubble';
    div.innerHTML = txt;
    stream.appendChild(div);
    stream.scrollTop = stream.scrollHeight;
}

function procesarRespuestaAsistente(pregunta) {
    let lower = pregunta.toLowerCase();
    let respuesta = currentLang === 'es' 
        ? "No te preocupes por eso. Si te piden un cargo extra que no entiendes, búscalo bien o ignóralo si no es obligatorio para volar."
        : "Don't worry about that. If they ask for an extra charge you don't understand, look closely or ignore it if it's not mandatory.";
    
    if (lower.includes("seguro") || lower.includes("proteccion") || lower.includes("insurance")) {
        respuesta = currentLang === 'es'
            ? "El seguro de la aerolínea siempre es opcional. Si no lo deseas, selecciona 'no gracias' para evitar cobros extra."
            : "Airline insurance is always optional. If you don't want it, select 'no thanks' to avoid extra charges.";
    } else if (lower.includes("maleta") || lower.includes("equipaje") || lower.includes("bag")) {
        respuesta = currentLang === 'es'
            ? "Verifica que el peso de tu maleta coincida con lo permitido para que no te cobren dinero de más al abordar."
            : "Verify that your bag's weight matches what's allowed to avoid paying extra money at the boarding gate.";
    }
    agregarMensajeChat("Copiloto: " + respuesta);
    speak(respuesta);
}

function handleClose() { 
    let confirmMsg = currentLang === 'es' ? "¿Desea finalizar la sesión? Los datos temporales se borrarán inmediatamente por seguridad." : "Do you wish to end the session? Temporary data will be erased immediately for security."; 
    if (confirm(confirmMsg)) { 
        window.location.href = "about:blank"; 
    } 
} 
</script> 
</body> 
</html> """ 

@app.get("/", response_class=HTMLResponse) 
async def home(): 
    return HTML_INDEX

@app.post("/traducir_itinerario") 
async def traducir_itinerario(request: Request): 
    return JSONResponse(content={"status": "ok"})
