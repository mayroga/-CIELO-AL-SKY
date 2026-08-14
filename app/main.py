import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI()

HTML_INDEX = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AL CIELO - Asistencia de Viaje Profesional</title>
    <style>
        body, html {
            margin: 0; padding: 0; height: 100%;
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #f4f6f9; color: #333;
        }
        .main-container {
            max-width: 680px;
            margin: 30px auto;
            padding: 25px;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        h1 { color: #004080; margin-top: 5px; font-size: 24px; }
        h2 { color: #004080; font-size: 20px; }
        button {
            padding: 12px 20px;
            margin: 6px;
            font-size: 15px;
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
        .btn-success { background-color: #28a745; color: white; border: none; font-size: 17px; padding: 14px 25px; box-shadow: 0 4px 10px rgba(40,167,69,0.3); }
        .btn-success:hover { background-color: #218838; }
        .hidden { display: none !important; }
        input, select {
            padding: 10px 12px;
            margin: 6px 0;
            font-size: 15px;
            width: 100%;
            box-sizing: border-box;
            border-radius: 6px;
            border: 1px solid #ccc;
            outline: none;
        }
        input:focus, select:focus { border-color: #004080; box-shadow: 0 0 5px rgba(0,64,128,0.2); }
        .error-message {
            color: #dc3545;
            font-weight: bold;
            margin: 8px 0;
            font-size: 14px;
        }
        #breathing-circle {
            width: 160px;
            height: 160px;
            background-color: #a8dadc;
            border-radius: 50%;
            margin: 15px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 15px;
            font-weight: bold;
            color: #fff;
            font-size: 13px;
            box-sizing: border-box;
            animation: respirarHumano 8s infinite ease-in-out;
        }
        @keyframes respirarHumano {
            0% { transform: scale(1.0); background-color: #a8dadc; }
            50% { transform: scale(1.3); background-color: #457b9d; }
            100% { transform: scale(1.0); background-color: #a8dadc; }
        }
        
        /* LAYOUT DIVIDIDO PARA VISTA DE TRABAJO CON GOOGLE FLIGHTS */
        .split-workspace {
            display: flex;
            width: 100vw;
            height: 100vh;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            overflow: hidden;
            background: #e9ecef;
        }
        .iframe-pane {
            flex: 2;
            height: 100%;
            background: #fff;
            border-right: 2px solid #ccc;
            position: relative;
        }
        .iframe-pane iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
        .copilot-pane {
            flex: 1;
            min-width: 340px;
            max-width: 420px;
            height: 100%;
            background: #fff;
            display: flex;
            flex-direction: column;
            box-shadow: -4px 0 15px rgba(0,0,0,0.1);
        }
        .copilot-header {
            background: #004080;
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 16px;
        }
        .copilot-body {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            font-size: 14px;
            background: #f8f9fa;
        }
        .chat-bubble {
            background: white;
            padding: 10px 14px;
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.04);
            line-height: 1.4;
            border-left: 4px solid #004080;
        }
        .copilot-footer {
            padding: 12px;
            background: #fff;
            border-top: 1px solid #e9ecef;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .control-row { display: flex; gap: 8px; align-items: center; }
        .btn-mic { background: #28a745; color: white; flex: 1; padding: 10px; font-size: 14px; }
        .btn-mic.muted { background: #dc3545; }
    </style>
</head>
<body>

<!-- CONTENEDOR PRINCIPAL DE CONFIGURACIÓN Y LEGAL -->
<div id="wrapper-setup-views">
    <div class="main-container">
        <div id="language-controls" style="text-align: right; margin-bottom: 10px;">
            <button onclick="setLanguage('es')" style="padding: 6px 12px; font-size: 13px;">Español</button>
            <button onclick="setLanguage('en')" style="padding: 6px 12px; font-size: 13px;">English</button>
        </div>

        <!-- VISTA 1: ACUERDO LEGAL OBLIGATORIO MAY ROGA LLC -->
        <div id="view-home">
            <h1 id="title">AL CIELO</h1>
            <p id="subtitle" style="font-size: 14px; line-height: 1.5; color: #444; margin: 12px 0; font-weight: bold;">
                Servicio Profesional Privado de Orientación, Acompañamiento y Blindaje contra Errores de Viaje.
            </p>
            
            <div style="text-align: left; background: #f8f9fa; border: 1px solid #ccc; padding: 14px; border-radius: 8px; max-height: 160px; overflow-y: auto; font-size: 12px; line-height: 1.4; margin: 15px 0; border-left: 5px solid #004080;">
                <p><strong>ACUERDO DE MANDATO Y PROTECCIÓN PERSONAL (MAY ROGA LLC):</strong></p>
                <p>Al presionar 'Acepto y Firmar Acuerdo', usted manifiesta de forma libre y voluntaria que:</p>
                <p>1. Solicita esta aplicación exclusivamente como su herramienta de ayuda personal para guiarle paso a paso, disipar dudas técnicas y protegerle contra confusiones o pérdidas de dinero al gestionar vuelos.</p>
                <p>2. Comprende que la aplicación actúa como un asesor consultivo de apoyo, brindándole instrucciones claras y sencillas para que usted tome el control final en las plataformas oficiales.</p>
                <p>3. Exime a May Roga LLC de responsabilidades ajenas a la orientación brindada, comprometiéndose a usar este sistema estrictamente para su asistencia personal.</p>
            </div>

            <div style="margin: 12px 0; font-size: 13px; font-weight: bold;">
                <input type="checkbox" id="chk-legal-accept" style="width: auto; margin-right: 8px;" onclick="evaluarAceptacionLegal()">
                <label for="chk-legal-accept" style="cursor:pointer;" id="lbl-accept-text">He leído, acepto el acuerdo y firmo para proteger mi proceso de viaje</label>
            </div>

            <div style="margin-top: 15px;">
                <button id="btn-entrar" class="btn-primary" onclick="iniciarRutaViaje()" disabled style="opacity: 0.5; cursor: not-allowed;">Acepto y Firmar Acuerdo</button>
                <button id="btn-cerrar" class="btn-danger" onclick="handleClose()">Cerrar</button>
            </div>
        </div>

        <!-- VISTA 2: FORMULARIO AVANZADO CON CAMPOS COMPLETOS PARA PRE-LLENAR GOOGLE FLIGHTS -->
        <div id="view-form" class="hidden">
            <h2 id="form-title">Itinerario y Preferencias de Vuelo</h2>
            <p id="form-desc" style="color: #666; font-size: 13px;">Ingrese los datos precisos para que Google Flights se abra prácticamente listo para su revisión final.</p>
            
            <div style="text-align: left; display: inline-block; width: 100%; font-size: 13px;">
                <div style="display: flex; gap: 10px;">
                    <div style="flex: 1;"><label id="lbl-origen" style="font-weight: bold; color: #004080;">Origen (IATA):</label><input type="text" id="origen" placeholder="Ej: MIA"></div>
                    <div style="flex: 1;"><label id="lbl-destino" style="font-weight: bold; color: #004080;">Destino (IATA):</label><input type="text" id="destino" placeholder="Ej: MAD"></div>
                </div>

                <div style="display: flex; gap: 10px; margin-top: 8px;">
                    <div style="flex: 1;"><label id="lbl-salida" style="font-weight: bold; color: #004080;">Fecha Salida:</label><input type="date" id="fecha_salida"></div>
                    <div style="flex: 1;"><label id="lbl-regreso" style="font-weight: bold; color: #004080;">Fecha Regreso (Opcional):</label><input type="date" id="fecha_regreso"></div>
                </div>

                <div style="display: flex; gap: 10px; margin-top: 8px;">
                    <div style="flex: 1;">
                        <label id="lbl-tipo" style="font-weight: bold; color: #004080;">Tipo de Viaje:</label>
                        <select id="tipo_viaje">
                            <option value="1">Ida y Vuelta / Round trip</option>
                            <option value="2">Ida / One way</option>
                            <option value="3">Multiciudad / Multi-city</option>
                        </select>
                    </div>
                    <div style="flex: 1;">
                        <label id="lbl-clase" style="font-weight: bold; color: #004080;">Clase:</label>
                        <select id="clase_asiento">
                            <option value="economy">Económica / Economy</option>
                            <option value="premium">Económica Premium</option>
                            <option value="business">Ejecutiva / Business</option>
                            <option value="first">Primera / First</option>
                        </select>
                    </div>
                </div>

                <div style="display: flex; gap: 10px; margin-top: 8px;">
                    <div style="flex: 1;"><label id="lbl-pasajeros" style="font-weight: bold; color: #004080;">Pasajeros (Adultos):</label><input type="number" id="pasajeros" value="1" min="1" max="9"></div>
                    <div style="flex: 1;"><label id="lbl-escala" style="font-weight: bold; color: #004080;">Escalas preferidas:</label>
                        <select id="escalas">
                            <option value="any">Cualquiera / Any</option>
                            <option value="1">Máximo 1 escala</option>
                            <option value="nonstop">Solo vuelos directos</option>
                        </select>
                    </div>
                </div>
            </div>

            <div id="error-box" class="error-message hidden"></div>
            
            <div style="margin-top: 20px;">
                <button class="btn-primary" id="btn-procesar" onclick="prepararConexionRespiratoria()">Continuar a Relajación y Activación</button>
                <button class="btn-danger" id="btn-cancelar" onclick="switchView('view-home')">Atrás</button>
            </div>
        </div>

        <!-- VISTA 3: CÍRCULO RESPIRATORIO + INSTRUCCIÓN CLARA + BOTÓN GOOGLE FLY -->
        <div id="view-loading" class="hidden">
            <h2 id="load-title">Preparando Tu Tranquilidad</h2>
            <p id="load-desc" style="color: #555; font-size: 13px; line-height: 1.4;">Inhala profundo. Suelta toda tensión. Estamos blindando tu proceso.</p>
            
            <!-- Círculo respiratorio secuencial único ordenado por kernel LocalStorage -->
            <div id="breathing-circle"><span id="breath-txt">Inhala calma</span></div>
            
            <div style="background: #e8f4fd; border: 1px solid #bbe1fa; padding: 10px; border-radius: 6px; font-size: 12px; color: #004080; margin: 10px 0; text-align: left; line-height: 1.4;">
                💡 <strong>AVISO IMPORTANTE PARA TI:</strong> Una vez que hagas clic en el botón verde de abajo, se abrirá Google Flights con tu ruta lista. En la ventana lateral podrás hablarme en todo momento con total confianza. Pregúntame con calma cualquier duda (asientos, maletas, tarifas); te responderé de forma sencilla y clara como un agente experto para cuidarte de cualquier error.
            </div>

            <!-- Botón obligatorio de activación manual de Google Fly -->
            <div style="margin-top: 15px;">
                <button class="btn-success" id="btn-conectar-google-fly" onclick="abrirEspacioTrabajoDividido()">✈️ ABRIR GOOGLE FLY Y COPILOTO PROTECTOR</button>
            </div>
        </div>
    </div>
</div>

<!-- VISTA 4: ESPACIO DE TRABAJO DIVIDIDO (PANTALLA PARTIDA) -->
<div id="view-split" class="split-workspace hidden">
    <!-- Panel Izquierdo: Google Flights Precargado -->
    <div class="iframe-pane">
        <iframe id="google-flights-frame" src="about:blank" title="Google Flights Oficial"></iframe>
    </div>

    <!-- Panel Derecho: Ventana de Copiloto Acompañante con Voz y Chat No Repetitivo -->
    <div class="copilot-pane">
        <div class="copilot-header">Copiloto Protector AL CIELO</div>
        <div class="copilot-body" id="chat-stream">
            <div class="chat-bubble">¡Hola! Ya tienes tus vuelos en pantalla. Respira tranquilo, estoy aquí contigo. Si tienes cualquier duda sobre algún precio, maleta o botón, háblame por el micrófono o escríbeme aquí mismo. Te guiaré paso a paso sin prisas.</div>
        </div>
        <div class="copilot-footer">
            <div class="control-row">
                <button id="btn-mic-toggle" class="btn-mic" onclick="toggleMic()">🎙️ Micrófono ON</button>
                <button class="btn-danger" onclick="handleClose()" style="font-size: 12px; padding: 10px;">Salir</button>
            </div>
            <div class="control-row">
                <input type="text" id="user-input-text" placeholder="Escribe tu duda aquí..." onkeypress="handleKey(event)" style="margin:0;">
                <button class="btn-primary" onclick="enviarTextoDuda()" style="margin:0; padding: 10px 14px;">Enviar</button>
            </div>
            <div style="font-size: 11px; color: #666; text-align: center; margin-top: 2px;">
                Asistencia privada bajo protección legal de May Roga LLC.
            </div>
        </div>
    </div>
</div>

<script>
let currentLang = 'es';
let micActive = true;
let recognition = null;
let urlGoogleFlightsGlobal = "https://www.google.com/travel/flights";
let breathInterval = null;
let voicedInstructionTriggered = false;

// Banco estricto de frases de relajación, antiagobio y antiestrés (orden numérico perfecto, sin repetición cíclica)
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
    "10. Recuerda que al abrir Google Fly podrás pedirme ayuda por voz con total confianza, esperando unos segundos para tu respuesta clara y sencilla."
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
    "10. Remember that once in Google Fly you can ask for voice help calmly, waiting a few seconds for your clear and simple answer."
];

function obtenerSiguienteFraseSecuencial() {
    let storageKey = "kernel_breath_index_" + currentLang;
    let indexStr = localStorage.getItem(storageKey);
    let currentIndex = indexStr ? parseInt(indexStr, 10) : 0;
    
    let banco = currentLang === 'es' ? frasesRelajacionES : frasesRelajacionEN;
    
    if (isNaN(currentIndex) || currentIndex < 0 || currentIndex >= banco.length) {
        currentIndex = 0;
    }
    
    let fraseSeleccionada = banco[currentIndex];
    let siguienteIndex = (currentIndex + 1) % banco.length;
    localStorage.setItem(storageKey, siguienteIndex.toString());
    
    return fraseSeleccionada;
}

function iniciarCicloRespiratorioDinamico() {
    if (breathInterval) clearInterval(breathInterval);
    let spanTxt = document.getElementById('breath-txt');
    
    let fraseActual = obtenerSiguienteFraseSecuencial();
    spanTxt.innerText = fraseActual;
    hablarVozClara(fraseActual);
    
    breathInterval = setInterval(() => {
        let proximaFrase = obtenerSiguienteFraseSecuencial();
        spanTxt.innerText = proximaFrase;
        hablarVozClara(proximaFrase);
    }, 9000);
}

const translations = {
    es: {
        title: "AL CIELO",
        subtitle: "Servicio Profesional Privado de Orientación, Acompañamiento y Blindaje contra Errores de Viaje.",
        acceptText: "He leído, acepto el acuerdo y firmo para proteger mi proceso de viaje",
        entrar: "Acepto y Firmar Acuerdo",
        cerrar: "Cerrar",
        formTitle: "Itinerario y Preferencias de Vuelo",
        formDesc: "Ingrese los datos precisos para que Google Flights se abra prácticamente listo para su revisión final.",
        lblOrigen: "Origen (IATA):",
        lblDestino: "Destino (IATA):",
        lblSalida: "Fecha Salida:",
        lblRegreso: "Fecha Regreso (Opcional):",
        lblTipo: "Tipo de Viaje:",
        lblClase: "Clase:",
        lblPasajeros: "Pasajeros (Adultos):",
        lblEscala: "Escalas preferidas:",
        procesar: "Continuar a Relajación y Activación",
        cancelar: "Atrás",
        loadTitle: "Preparando Tu Tranquilidad",
        loadDesc: "Inhala profundo. Suelta toda tensión. Estamos blindando tu proceso."
    },
    en: {
        title: "TO THE SKY",
        subtitle: "Private Professional Guidance and Travel Shielding Service.",
        acceptText: "I have read, accept the agreement and sign to protect my travel process",
        entrar: "Accept & Sign Agreement",
        cerrar: "Close",
        formTitle: "Itinerary & Flight Preferences",
        formDesc: "Enter precise details so Google Flights opens almost ready for your final review.",
        lblOrigen: "Origin (IATA):",
        lblDestino: "Destination (IATA):",
        lblSalida: "Departure Date:",
        lblRegreso: "Return Date (Optional):",
        lblTipo: "Trip Type:",
        lblClase: "Class:",
        lblPasajeros: "Passengers (Adults):",
        lblEscala: "Preferred Stops:",
        procesar: "Continue to Relaxation & Activation",
        cancelar: "Back",
        loadTitle: "Preparing Your Peace of Mind",
        loadDesc: "Inhale deep. Release all tension. We are shielding your process."
    }
};

function setLanguage(lang) {
    currentLang = lang;
    let t = translations[lang];
    document.getElementById('title').innerText = t.title;
    document.getElementById('subtitle').innerText = t.subtitle;
    document.getElementById('lbl-accept-text').innerText = t.acceptText;
    document.getElementById('btn-entrar').innerText = t.entrar;
    document.getElementById('btn-cerrar').innerText = t.cerrar;
    document.getElementById('form-title').innerText = t.formTitle;
    document.getElementById('form-desc').innerText = t.formDesc;
    document.getElementById('lbl-origen').innerText = t.lblOrigen;
    document.getElementById('lbl-destino').innerText = t.lblDestino;
    document.getElementById('lbl-salida').innerText = t.lblSalida;
    document.getElementById('lbl-regreso').innerText = t.lblRegreso;
    document.getElementById('lbl-tipo').innerText = t.lblTipo;
    document.getElementById('lbl-clase').innerText = t.lblClase;
    document.getElementById('lbl-pasajeros').innerText = t.lblPasajeros;
    document.getElementById('lbl-escala').innerText = t.lblEscala;
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
        document.getElementById('view-split').classList.remove('hidden');
    } else {
        document.getElementById('wrapper-setup-views').classList.remove('hidden');
        document.getElementById(viewId).classList.remove('hidden');
    }
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
    hablarVozClara(currentLang === 'es' ? "Por favor completa los datos de tu vuelo para dejarlo listo." : "Please fill in your flight details to get it ready.");
}

/* Síntesis de voz clara, fuerte, fácil de entender (para niño de 8 años / adulto estresado) */
function hablarVozClara(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        let textoLimpio = text.replace(/<\/?[^>]+(>|$)/g, "").replace(/•/g, "").replace(/➔/g, "hacia").replace(/^\d+\.\s*/, "");
        let utterance = new SpeechSynthesisUtterance(textoLimpio);
        utterance.lang = currentLang === 'es' ? 'es-ES' : 'en-US';
        utterance.rate = 0.90; // Pausado, claro y firme
        utterance.pitch = 1.0; 
        window.speechSynthesis.speak(utterance);
    }
}

function prepararConexionRespiratoria() {
    let org = document.getElementById('origen').value.trim();
    let dest = document.getElementById('destino').value.trim();
    let depDate = document.getElementById('fecha_salida').value;
    let retDate = document.getElementById('fecha_regreso').value;
    let tripType = document.getElementById('tipo_viaje').value;
    let pax = document.getElementById('pasajeros').value;
    let errBox = document.getElementById('error-box');

    if (!org || !dest) {
        let msg = currentLang === 'es' ? "Por favor ingresa al menos el origen y el destino." : "Please enter at least origin and destination.";
        errBox.innerText = msg;
        errBox.classList.remove('hidden');
        hablarVozClara(msg);
        return;
    }
    errBox.classList.add('hidden');
    
    // Construcción avanzada de URL para Google Flights con parámetros completos para evitar que el cliente tenga que rellenar
    let o = org.toUpperCase().substring(0, 3);
    let d = dest.toUpperCase().substring(0, 3);
    
    // URL estructurada de Google Flights con parámetros de búsqueda avanzados
    let queryParams = `flights from ${o} to ${d}`;
    if (depDate) queryParams += ` on ${depDate}`;
    if (retDate && tripType === "1") queryParams += ` returning ${retDate}`;
    
    urlGoogleFlightsGlobal = `https://www.google.com/travel/flights?q=${encodeURIComponent(queryParams)}`;

    switchView('view-loading');
    iniciarCicloRespiratorioDinamico();
}

// CONEXIÓN MANUAL ESTRICTA: Solo ocurre al dar clic en el botón de Google Fly
function abrirEspacioTrabajoDividido() {
    if (breathInterval) {
        clearInterval(breathInterval);
        breathInterval = null;
    }
    
    // Cambiar a la vista dividida
    switchView('view-split');
    
    // Cargar la URL pre-llenada en el iframe izquierdo
    document.getElementById('google-flights-frame').src = urlGoogleFlightsGlobal;
    
    // Iniciar asistencia de voz y chat protector en el panel derecho
    iniciarReconocimientoVoz();
    
    let bienvenidaCopiloto = currentLang === 'es'
        ? "Ya estamos en Google Flights. Respira hondo. Si te sale una tarifa que no entiendes o un recargo de maleta, pregúntame aquí con confianza. Te responderé de forma muy sencilla."
        : "We are now in Google Flights. Take a deep breath. If you see a fare you don't understand, ask me here with confidence. I will answer simply.";
    
    agregarMensajeChat("Copiloto: " + bienvenidaCopiloto);
    hablarVozClara(bienvenidaCopiloto);
}

function iniciarReconocimientoVoz() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) return;
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
    if (micActive) {
        btn.innerText = currentLang === 'es' ? "🎙️ Micrófono ON" : "🎙️ Mic ON";
        btn.classList.remove('muted');
        if(recognition) try { recognition.start(); } catch(e) {}
        hablarVozClara(currentLang === 'es' ? "Micrófono encendido." : "Microphone on.");
    } else {
        btn.innerText = currentLang === 'es' ? "🔇 Micrófono OFF" : "🔇 Mic OFF";
        btn.classList.add('muted');
        if(recognition) recognition.stop();
        hablarVozClara(currentLang === 'es' ? "Micrófono apagado, puedes leer con calma." : "Microphone off.");
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
    stream.scrollTop = stream.scrollHeight;
}

function procesarRespuestaAsistente(pregunta) {
    let lower = pregunta.toLowerCase();
    let respuesta = currentLang === 'es' 
        ? "No te preocupes. Lee con calma las opciones en pantalla. Si te piden un seguro o maleta extra que no necesitas, desmárcalo para ahorrar dinero. ¿Quieres que veamos otra fecha?"
        : "Don't worry. Read the options on screen calmly. If they ask for insurance you don't need, uncheck it to save money.";
    
    if (lower.includes("seguro") || lower.includes("proteccion") || lower.includes("insurance")) {
        respuesta = currentLang === 'es'
            ? "El seguro opcional se puede quitar. Búscalo en la pantalla y desmárcalo si prefieres no pagarlo."
            : "Optional insurance can be removed. Look for it on screen and uncheck it if you prefer not to pay.";
    } else if (lower.includes("maleta") || lower.includes("equipaje") || lower.includes("bag")) {
        respuesta = currentLang === 'es'
            ? "Revisa que tu tarifa incluya equipaje de mano. Si solo llevas mochila personal, la tarifa básica es tu mejor opción para gastar menos."
            : "Check if your fare includes carry-on luggage. If you only carry a personal backpack, the basic fare is best to spend less.";
    }
    
    agregarMensajeChat("Copiloto: " + respuesta);
    hablarVozClara(respuesta);
}

function handleClose() { 
    let confirmMsg = currentLang === 'es' ? "¿Deseas salir? Tus datos temporales se borrarán de inmediato para proteger tu privacidad." : "Do you wish to exit? Temporary data will be cleared immediately."; 
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
