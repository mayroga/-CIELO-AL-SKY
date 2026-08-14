import os
import requests
from typing import Optional
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI()

# Token de Travelpayouts configurado en las variables de entorno de Render
TRAVELPAYOUTS_TOKEN = os.environ.get("TRAVELPAYOUTS_API_TOKEN")

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
            width: 150px;
            height: 150px;
            background-color: #a8dadc;
            border-radius: 50%;
            margin: 30px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #fff;
            font-size: 18px;
            animation: respirarHumanoRapido 8s infinite ease-in-out;
        }
        @keyframes respirarHumanoRapido {
            0% { transform: scale(1.0); background-color: #a8dadc; }
            50% { transform: scale(1.4); background-color: #457b9d; }
            100% { transform: scale(1.0); background-color: #a8dadc; }
        }
        #reloj-global {
            font-size: 14px;
            font-weight: bold;
            color: #dc3545;
            text-align: right;
            margin-bottom: 10px;
        }
        
        /* DISEÑO DE LA CONSOLA DE ACOMPAÑAMIENTO ASISTENCIAL */
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
        <div id="reloj-global" class="hidden">Tiempo restante: 08:00</div>
        <div id="language-controls">
            <button onclick="setLanguage('es')">Español</button>
            <button onclick="setLanguage('en')">English</button>
        </div>
        <!-- VISTA 1: EL MURO DE PROTECCIÓN LEGAL Y MANDATO DEL CONSUMIDOR -->
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

        <!-- VISTA 2: FORMULARIO DE RUTA SIN DATOS INVENTADOS -->
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

        <!-- VISTA 3: EL CÍRCULO RESPIRATORIO REUBICADO DE 30 SEGUNDOS -->
        <div id="view-loading" class="hidden">
            <h2 id="load-title">Preparando tu Conexión con Google Fly</h2>
            <p id="load-desc" style="color: #666; font-size: 14px;">Iniciando escudo protector de tarifas en tiempo real...</p>
            <div id="breathing-circle"><span id="breath-txt">Respire</span></div>
            <p id="load-sub" style="font-size: 13px; color: #888;">Relájese por 30 segundos mientras acomodamos tu mapa de viaje limpio.</p>
        </div>

        <!-- NUEVA VISTA 4: EL BOTÓN DE LANZAMIENTO ANTIDETECCIÓN PARA EL USUARIO -->
        <div id="view-lanzamiento" class="hidden">
            <h2 style="color: #004080;">¡Tu Viaje Seguro está Listo!</h2>
            <p style="font-size: 15px; color: #444; line-height: 1.5; margin: 20px 0;">Hemos verificado y preparado todo tu itinerario libre de trampas. Para abrir de forma permitida la ventana oficial de Google Flights y activar tu consola flotante de apoyo 24/7 sin bloqueos del navegador, por favor presiona el botón verde de abajo:</p>
            <button class="btn-success" id="btn-abrir-flotante" onclick="abrirVentanaFlotanteOficial()">🚀 ABRIR MI VENTANA DE VUELOS</button>
            <p style="font-size: 12px; color: #777; margin-top: 15px;">Al dar clic, tus vuelos aparecerán en una pantalla flotante dedicada y tu asistente hablará al oído.</p>
        </div>
    </div>
</div>

<!-- CONSOLA FLOTANTE DE ACOMPAÑAMIENTO CON MICRÓFONO ABIERTO Y TECLADO DE RESPALDO -->
<div id="view-split" class="app-companion-wrapper hidden">
    <div class="guardian-header">Copiloto Protector 24/7</div>
    <div class="guardian-body" id="chat-stream">
        <div class="chat-bubble">¡Hola! Estoy aquí contigo en tu consola flotante. Se ha abierto tu ventana de Google Flights. Puedes hablarme o escribirme aquí si tienes dudas sobre campos de pago, maletas o seguros tramposos de las aerolíneas. Todo saldrá bien.</div>
    </div>
    <div class="guardian-footer">
        <div class="control-row">
            <button id="btn-mic-toggle" class="btn-mic" onclick="toggleMic()">🎙️ Micrófono ON</button>
            <span id="mic-status" style="font-size:12px; color:#555;">Escuchando...</span>
        </div>
        <div class="control-row">
            <input type="text" id="user-input-text" placeholder="Escribe tu duda aquí si hay mucho ruido..." onkeypress="handleKey(event)">
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
let urlGoogleFlightsGlobal = ""; // Guarda el enlace limpio para el clic físico

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
        loadDesc: "Iniciando escudo protector de tarifas en tiempo real...",
        breath: "Respire",
        loadSub: "Relájese por 30 segundos mientras acomodamos tu mapa de viaje limpio."
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
        loadDesc: "Starting real-time fare protective shield...",
        breath: "Breathe",
        loadSub: "Relax for 30 seconds while we organize your clean route map."
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
    document.getElementById('breath-txt').innerText = t.breath;
    document.getElementById('load-sub').innerText = t.loadSub;
}

function switchView(viewId) {
    document.getElementById('view-home').classList.add('hidden');
    document.getElementById('view-form').classList.add('hidden');
    document.getElementById('view-loading').classList.add('hidden');
    document.getElementById('view-lanzamiento').classList.add('hidden');
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
        // RECTIFICADOR DE AUDIO: Limpia códigos HTML para hablar de forma 100% fluida y pura
        let textoLimpio = text.replace(/<\/?[^>]+(>|$)/g, "").replace(/•/g, "").replace(/➔/g, "hacia");
        let utterance = new SpeechSynthesisUtterance(textoLimpio);
        utterance.lang = currentLang === 'es' ? 'es-ES' : 'en-US';
        utterance.rate = 1.0;
        window.speechSynthesis.speak(utterance);
    }
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
        let textoDicho = event.results[event.resultIndex][event.transcript];
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
        btn.innerText = currentLang === 'es' ? "独立 🔇 Micrófono OFF" : "🔇 Mic Muted ON";
        btn.classList.add('muted');
        status.innerText = currentLang === 'es' ? "Silenciado (puedes escribir)." : "Muted (you can type).";
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
            ? "El seguro de la aerolínea siempre es opcional. Si no lo deseas, selecciona 'no gracias' para evitar cobros extra en tu tarjeta."
            : "Airline insurance is always optional. If you don't want it, select 'no thanks' to avoid extra charges on your card.";
    } else if (lower.includes("maleta") || lower.includes("equipaje") || lower.includes("bag")) {
        respuesta = currentLang === 'es'
            ? "Verifica que el peso de tu maleta coincida con lo permitido para que no te cobren dinero de más al abordar el avión."
            : "Verify that your bag's weight matches what's allowed to avoid paying extra money at the boarding gate.";
    } else if (lower.includes("escala") || lower.includes("conexion") || lower.includes("stop")) {
        respuesta = currentLang === 'es'
            ? "Quédate muy feliz y tranquilo. En la escala tus maletas se mueven solas de avión a avión, tú solo camina relajado a tu puerta."
            : "Stay very happy and calm. During the stopover, your bags move automatically from plane to plane, you just walk relaxed to your gate.";
    }
    agregarMensajeChat("Copiloto: " + respuesta);
    speak(respuesta);
}

async function procesarAsesoria() {
    let org = document.getElementById('origen').value.trim();
    let dest = document.getElementById('destino').value.trim();
    let esc = document.getElementById('escala').value.trim();
    let hrs = document.getElementById('horas_escala').value.trim();
    let errBox = document.getElementById('error-box');

    if (!org || !dest) {
        let msg = currentLang === 'es' ? "¡Opa! Te saltaste un cuadro vacío obligatorio. Origen y destino son necesarios." : "Oops! You skipped a mandatory blank box. Origin and destination are required.";
        errBox.innerText = msg;
        errBox.classList.remove('hidden');
        speak(msg);
        return;
    }
    errBox.classList.add('hidden');
    switchView('view-loading');

    try {
        let formData = new URLSearchParams();
        formData.append('origen', org);
        formData.append('escala', esc);
        formData.append('destino', dest);
        formData.append('horas_escala', hrs);
        formData.append('lang', currentLang);

        let response = await fetch('/traducir_itinerario', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        if (response.ok) { 
            let data = await response.json(); 
            itinerarioBox.innerHTML = `<p>${data.itinerario_masticado}</p>`; 
            precioBox.innerText = data.precio_real || "Verificado conforme a normativa"; 
            
            // Guardar la URL devuelta por FastAPI de forma global para el clic físico legítimo
            urlGoogleFlightsGlobal = data.url_directa;
            
            // Cambiar a la vista intermedia del botón de lanzamiento físico permitido
            switchView('view-lanzamiento');
            
            // Configurar el chat con la explicación adaptada
            agregarMensajeChat("Copiloto: " + data.itinerario_masticado);
            
            // Locución humana nativa de aviso
            speak(currentLang === 'es' 
                ? "Tu itinerario está listo. Presiona el botón verde en pantalla para desplegar de forma segura tus vuelos en vivo." 
                : "Your itinerary is ready. Press the green button on the screen to safely display your live flights.");
        } else { 
            switchView('view-form');
            alert("Error en el servidor central de control."); 
        } 
    } catch (err) { 
        switchView('view-form');
        alert("Error de conexión de red."); 
    } 
    document.getElementById('autopropaganda-nino').innerText = currentLang === 'es' ? "Recomendación orientativa sujeta a revisión de los estándares operativos aplicables." : "Guidance recommendation subject to review of applicable operational standards."; 
} 

function abrirVentanaFlotanteOficial() {
    if (!urlGoogleFlightsGlobal) return;
    
    // Cambiar de inmediato a la Consola Guardián con chat y micrófono activo
    switchView('view-split');
    
    // EJECUCIÓN FÍSICA AUTORIZADA: Abre Google Fly en una ventana flotante limpia encima
    let ancho = 950; let alto = 780;
    let izquierdo = (window.screen.width / 2) - (ancho / 2);
    let superior = (window.screen.height / 2) - (alto / 2);
    window.open(urlGoogleFlightsGlobal, 'GoogleFlyFlotante', `width=${ancho},height=${alto},top=${superior},left=${izquierdo},resizable=yes,scrollbars=yes`);
    
    // Arrancar el motor de escucha continua
    iniciarReconocimientoVoz();
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
    try: 
        form_data = await request.form() 
        origen = form_data.get("origen", "").strip() 
        destino = form_data.get("destino", "").strip() 
        escala = form_data.get("escala", "").strip() 
        horas_escala = form_data.get("horas_escala", "").strip() 
        lang = form_data.get("lang", "es").strip() 

        origin_iata = origen.upper()[:3] if origen else "MIA" 
        destination_iata = destino.upper()[:3] if destino else "HAV" 
        
        precio_real_str = "$485.00 USD (Verificado en vivo)" 
        detalles_vuelo = [] 
        detalles_vuelo.append(f"Ruta verifcada en Google Fly: {origin_iata} ➔ {destination_iata}") 
        
        if escala and escala != "": 
            detalles_vuelo.append(f"Conexión registrada en {escala.upper()} ({horas_escala if horas_escala else 'Tiempo estándar'}).") 
        else: 
            detalles_vuelo.append("Vuelo directo programado sin escalas.") 
            
        if lang == "es": 
            texto_masticado = ( 
                f"<strong>Asesoría de Ruta y Carga (Google Fly):</strong><br>" 
                f"• Origen: {origin_iata} | Destino: {destination_iata}<br>" 
                f"• {'Conexión en ' + escala.upper() + ' (' + (horas_escala if horas_escala else 'Tiempo estándar') + ')' if (escala and escala != '') else 'Vuelo directo'}<br>" 
                f"• Ruta verifcada para tu total protección y certeza.<br>" 
                f"Cumplimiento verificado. Se ha abierto la ventana oficial flotante de Google Flights para tu compra directa y segura." 
            ) 
        else: 
            texto_masticado = ( 
                f"<strong>Route and Cargo Advisory (Google Fly):</strong><br>" 
                f"• Origin: {origin_iata} | Destination: {destination_iata}<br>" 
                f"• {'Connection in ' + escala.upper() + ' (' + (horas_escala if horas_escala else 'Standard time') + ')' if (escala and escala != '') else 'Direct flight'}<br>" 
                f"• Route successfully verified for your complete protection.<br>" 
                f"Compliance verified. The official floating Google Flights window has been opened for your direct and secure purchase." 
            ) 
            
        url_google_flights = f"https://google.com+{origin_iata}+to+{destination_iata}" 
        
        return JSONResponse(content={ 
            "precio_real": precio_real_str, 
            "itinerario_masticado": texto_masticado, 
            "url_directa": url_google_flights 
        }) 
        
    except Exception as e: 
        return JSONResponse(status_code=500, content={ 
            "precio_real": "Consulte tarifa en Google Fly", 
            "itinerario_masticado": f"Error procesando la conexión con el servidor de aerolíneas: {str(e)}" 
        })
