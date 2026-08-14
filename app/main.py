import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_INDEX = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AL CIELO - Asistencia Profesional de Viaje</title>
    <style>
        body, html {
            margin: 0; padding: 0; height: 100%;
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #f4f6f9; color: #333;
        }
        .main-container {
            max-width: 720px;
            margin: 25px auto;
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
        /* Consola de acompañamiento invisible/discreta fuera de Google para no interferir jamás */
        #companion-console {
            margin-top: 15px;
            padding: 12px;
            background: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 13px;
            text-align: left;
        }
    </style>
</head>
<body>

<div class="main-container" id="setup-container">
    <div style="text-align: right; margin-bottom: 10px;">
        <button onclick="setLanguage('es')" style="padding: 6px 12px; font-size: 13px;">Español</button>
        <button onclick="setLanguage('en')" style="padding: 6px 12px; font-size: 13px;">English</button>
    </div>

    <!-- VISTA 1: ACUERDO LEGAL MAY ROGA LLC -->
    <div id="view-home">
        <h1 id="title">AL CIELO</h1>
        <p id="subtitle" style="font-size: 14px; line-height: 1.5; color: #444; margin: 12px 0; font-weight: bold;">
            Servicio Profesional Privado de Orientación, Acompañamiento y Blindaje contra Errores de Viaje.
        </p>
        
        <div style="text-align: left; background: #f8f9fa; border: 1px solid #ccc; padding: 14px; border-radius: 8px; max-height: 160px; overflow-y: auto; font-size: 12px; line-height: 1.4; margin: 15px 0; border-left: 5px solid #004080;">
            <p><strong>ACUERDO DE MANDATO Y PROTECCIÓN PERSONAL (MAY ROGA LLC):</strong></p>
            <p>Al presionar 'Acepto y Firmar Acuerdo', usted manifiesta de forma libre y voluntaria que:</p>
            <p>1. Solicita esta aplicación exclusivamente como su herramienta de ayuda personal para guiarle paso a paso.</p>
            <p>2. Comprende que la aplicación actúa como un asesor consultivo de apoyo.</p>
            <p>3. Exime a May Roga LLC de responsabilidades ajenas a la orientación brindada.</p>
        </div>

        <div style="margin: 12px 0; font-size: 13px; font-weight: bold;">
            <input type="checkbox" id="chk-legal-accept" style="width: auto; margin-right: 8px;" onclick="evaluarAceptacionLegal()">
            <label for="chk-legal-accept" style="cursor:pointer;" id="lbl-accept-text">He leído, acepto el acuerdo y firmo para proteger mi proceso de viaje</label>
        </div>

        <div style="margin-top: 15px;">
            <button id="btn-entrar" class="btn-primary" onclick="iniciarRutaViaje()" disabled style="opacity: 0.5; cursor: not-allowed;">Acepto y Firmar Acuerdo</button>
            <button class="btn-danger" onclick="handleClose()">Cerrar</button>
        </div>
    </div>

    <!-- VISTA 2: FORMULARIO COMPLETO PARA PRELLENAR BÚSQUEDA -->
    <div id="view-form" class="hidden">
        <h2 id="form-title">Datos Completos para Automatización de Vuelo</h2>
        <p id="form-desc" style="color: #666; font-size: 13px;">Llene estos campos detallados para configurar su búsqueda con total precisión, certeza y seguridad antes de abrir Google Flights.</p>
        
        <div style="text-align: left; display: inline-block; width: 100%; font-size: 13px;">
            <div style="display: flex; gap: 10px;">
                <div style="flex: 1;"><label id="lbl-origen" style="font-weight: bold; color: #004080;">Origen (IATA):</label><input type="text" id="origen" placeholder="Ej: MIA"></div>
                <div style="flex: 1;"><label id="lbl-destino" style="font-weight: bold; color: #004080;">Destino (IATA):</label><input type="text" id="destino" placeholder="Ej: MAD"></div>
            </div>

            <div style="display: flex; gap: 10px; margin-top: 8px;">
                <div style="flex: 1;"><label id="lbl-salida" style="font-weight: bold; color: #004080;">Fecha Salida:</label><input type="date" id="fecha_salida"></div>
                <div style="flex: 1;"><label id="lbl-regreso" style="font-weight: bold; color: #004080;">Fecha Regreso:</label><input type="date" id="fecha_regreso"></div>
            </div>

            <div style="display: flex; gap: 10px; margin-top: 8px;">
                <div style="flex: 1;">
                    <label id="lbl-tipo" style="font-weight: bold; color: #004080;">Tipo de Viaje:</label>
                    <select id="tipo_viaje">
                        <option value="1">Ida y Vuelta</option>
                        <option value="2">Ida Sola</option>
                        <option value="3">Multiciudad</option>
                    </select>
                </div>
                <div style="flex: 1;">
                    <label id="lbl-clase" style="font-weight: bold; color: #004080;">Clase de Asiento:</label>
                    <select id="clase_asiento">
                        <option value="economy">Económica</option>
                        <option value="premium">Económica Premium</option>
                        <option value="business">Ejecutiva (Business)</option>
                        <option value="first">Primera Clase</option>
                    </select>
                </div>
            </div>

            <div style="display: flex; gap: 10px; margin-top: 8px;">
                <div style="flex: 1;"><label id="lbl-pasajeros" style="font-weight: bold; color: #004080;">Pasajeros Adultos:</label><input type="number" id="pasajeros" value="1" min="1" max="9"></div>
                <div style="flex: 1;"><label id="lbl-ninos" style="font-weight: bold; color: #004080;">Niños / Infantes:</label><input type="number" id="ninos" value="0" min="0" max="6"></div>
            </div>

            <div style="display: flex; gap: 10px; margin-top: 8px;">
                <div style="flex: 1;"><label id="lbl-aerolinea" style="font-weight: bold; color: #004080;">Aerolínea Preferida (Opcional):</label><input type="text" id="aerolinea" placeholder="Ej: American, Avianca, etc."></div>
                <div style="flex: 1;"><label id="lbl-equipaje" style="font-weight: bold; color: #004080;">Equipaje esperado:</label>
                    <select id="equipaje">
                        <option value="carryon">Mochila + Maleta de mano</option>
                        <option value="checked">Incluir maleta documentada</option>
                        <option value="basic">Solo objeto personal</option>
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

    <!-- VISTA 3: RELAJACIÓN Y APERTURA DE GOOGLE EN PESTAÑA LIBRE (CON CONSOLA DE APOYO EN SEGUNDO PLANO) -->
    <div id="view-loading" class="hidden">
        <h2 id="load-title">Preparando Tu Tranquilidad</h2>
        <p id="load-desc" style="color: #555; font-size: 13px; line-height: 1.4;">Inhala profundo. Al abrir Google Flights en pestaña libre, esta pestaña mantendrá su micrófono inteligente activo por detrás para escucharte, apoyarte y acompañarte en todo lo que necesites sin tocar ni invadir Google.</p>
        
        <div id="breathing-circle"><span id="breath-txt">Inhala calma</span></div>
        
        <div id="companion-console">
            <p style="margin: 0 0 6px 0; color: #004080; font-weight: bold;">🎙️ Centro de Acompañamiento por Voz en Segundo Plano:</p>
            <p id="status-mic-text" style="margin: 0; color: #28a745; font-weight: bold;">● Micrófono Inteligente Abierto y Escuchando</p>
            <p style="margin: 6px 0 0 0; font-size: 12px; color: #666;">Di <em>"Pausa"</em> o <em>"Pause"</em> para silenciar, o <em>"Continúa"</em> o <em>"Continue"</em> para reactivar. Si hablas de vuelos, equipaje, conexiones o dudas, el asesor te apoyará al instante. Si hablas de otro tema ajeno, guardará silencio absoluto.</p>
        </div>

        <div style="margin-top: 15px;">
            <button class="btn-success" onclick="abrirGooglePestanaLibreYActivarAsistente()">✈️ ABRIR GOOGLE FLIGHTS EN PESTAÑA LIBRE</button>
        </div>
    </div>
</div>

<script>
let currentLang = 'es';
let micActive = true;
let recognition = null;
let urlGoogleFlightsGlobal = "https://www.google.com/travel/flights";
let breathInterval = null;

const frasesRelajacionES = [
    "1. Inhala despacio y suelta cualquier carga mental.",
    "2. Cada respiración te devuelve la paz y el control total.",
    "3. No hay prisa; tu camino está seguro hoy.",
    "4. Suelta la tensión; todo está saliendo bien.",
    "5. Respira hondo y confía en tu viaje.",
    "6. La tranquilidad es tu mayor aliada.",
    "7. Un paso a la vez, tu mente descansa.",
    "8. Libera el agobio; mereces un viaje sin estrés.",
    "9. Siente el aire puro llenando tu interior.",
    "10. Recuerda que puedes decir 'Pausa' o 'Continúa' en cualquier momento."
];

const frasesRelajacionEN = [
    "1. Inhale slowly and release any heavy burden.",
    "2. Each breath brings back your absolute peace.",
    "3. There is no rush; your journey is safe.",
    "4. Release tension; everything is fine.",
    "5. Take a deep breath and trust.",
    "6. Tranquility is your greatest ally.",
    "7. One step at a time, your mind rests.",
    "8. Let go of overwhelm; enjoy a calm trip.",
    "9. Feel pure air filling your inner self.",
    "10. Remember you can say 'Pause' or 'Continue' anytime."
];

function obtenerSiguienteFraseSecuencial() {
    let storageKey = "kernel_breath_index_" + currentLang;
    let indexStr = localStorage.getItem(storageKey);
    let currentIndex = indexStr ? parseInt(indexStr, 10) : 0;
    let banco = currentLang === 'es' ? frasesRelajacionES : frasesRelajacionEN;
    if (isNaN(currentIndex) || currentIndex < 0 || currentIndex >= banco.length) currentIndex = 0;
    let frase = banco[currentIndex];
    localStorage.setItem(storageKey, ((currentIndex + 1) % banco.length).toString());
    return frase;
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

function switchView(viewId) {
    if (viewId !== 'view-loading' && breathInterval) {
        clearInterval(breathInterval);
        breathInterval = null;
    }
    document.getElementById('view-home').classList.add('hidden');
    document.getElementById('view-form').classList.add('hidden');
    document.getElementById('view-loading').classList.add('hidden');
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
    hablarVozClara(currentLang === 'es' ? "Por favor completa los datos detallados de tu viaje." : "Please fill in your detailed travel data.");
}

function hablarVozClara(text) {
    if (!micActive) return;
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        let textoLimpio = text.replace(/<\/?[^>]+(>|$)/g, "").replace(/^\d+\.\s*/, "");
        let utterance = new SpeechSynthesisUtterance(textoLimpio);
        utterance.lang = currentLang === 'es' ? 'es-ES' : 'en-US';
        utterance.rate = 0.90;
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
    let ninos = document.getElementById('ninos').value;
    let airline = document.getElementById('aerolinea').value.trim();
    let errBox = document.getElementById('error-box');

    if (!org || !dest) {
        let msg = currentLang === 'es' ? "Por favor ingresa al menos el origen y el destino." : "Please enter at least origin and destination.";
        errBox.innerText = msg;
        errBox.classList.remove('hidden');
        hablarVozClara(msg);
        return;
    }
    errBox.classList.add('hidden');
    
    let o = org.toUpperCase().substring(0, 3);
    let d = dest.toUpperCase().substring(0, 3);
    
    let queryParams = `flights from ${o} to ${d}`;
    if (depDate) queryParams += ` on ${depDate}`;
    if (retDate && tripType === "1") queryParams += ` returning ${retDate}`;
    if (airline) queryParams += ` airline ${airline}`;
    let totalPax = parseInt(pax) + parseInt(ninos);
    queryParams += ` passengers ${totalPax}`;
    
    urlGoogleFlightsGlobal = `https://www.google.com/travel/flights?q=${encodeURIComponent(queryParams)}`;

    switchView('view-loading');
    iniciarCicloRespiratorioDinamico();
}

function abrirGooglePestanaLibreYActivarAsistente() {
    if (breathInterval) {
        clearInterval(breathInterval);
        breathInterval = null;
    }
    
    // Abre Google Flights en pestaña totalmente independiente y libre (cero interferencias en Google)
    window.open(urlGoogleFlightsGlobal, '_blank');
    
    // Inicia el reconocimiento inteligente en esta pestaña de asesoría en segundo plano
    iniciarReconocimientoVozInteligente();
    hablarVozClara(currentLang === 'es' ? "Google Flights abierto. Estoy aquí en segundo plano escuchándote para apoyarte." : "Google Flights opened. I am here in the background listening to support you.");
}

function iniciarReconocimientoVozInteligente() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) return;
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRec();
    recognition.lang = currentLang === 'es' ? 'es-ES' : 'en-US';
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
        let textoDicho = event.results[event.resultIndex][0].transcript.toLowerCase().trim();
        
        // 1. Control de pausa / continuar por voz
        if (textoDicho.includes("pausa") || textoDicho.includes("pause") || textoDicho.includes("silencio") || textoDicho.includes("stop")) {
            micActive = false;
            document.getElementById('status-mic-text').innerText = currentLang === 'es' ? "● Micrófono en Pausa" : "● Microphone Paused";
            document.getElementById('status-mic-text').style.color = "#dc3545";
            hablarVozClara(currentLang === 'es' ? "Micrófono en pausa." : "Microphone paused.");
            return;
        }
        
        if (textoDicho.includes("continúa") || textoDicho.includes("continua") || textoDicho.includes("continue") || textoDicho.includes("enciende") || textoDicho.includes("start")) {
            micActive = true;
            document.getElementById('status-mic-text').innerText = currentLang === 'es' ? "● Micrófono Inteligente Abierto y Escuchando" : "● Smart Microphone Open & Listening";
            document.getElementById('status-mic-text').style.color = "#28a745";
            hablarVozClara(currentLang === 'es' ? "Micrófono reactivado." : "Microphone active.");
            return;
        }

        if (!micActive) return;

        // 2. Filtro estricto: Solo responde si la consulta está relacionada con vuelos, viajes, equipaje, conexiones o asistencia. Si es ajeno, silencio total.
        let esTemaDeVuelo = 
            textoDicho.includes("vuelo") || textoDicho.includes("flight") ||
            textoDicho.includes("maleta") || textoDicho.includes("bag") || textoDicho.includes("equipaje") ||
            textoDicho.includes("precio") || textoDicho.includes("price") || textoDicho.includes("asiento") || textoDicho.includes("seat") ||
            textoDicho.includes("escala") || textoDicho.includes("layover") || textoDicho.includes("aerolínea") || textoDicho.includes("airline") ||
            textoDicho.includes("seguro") || textoDicho.includes("insurance") || textoDicho.includes("pago") || textoDicho.includes("pay") ||
            textoDicho.includes("ayuda") || textoDicho.includes("help") || textoDicho.includes("duda") || textoDicho.includes("question") ||
            textoDicho.includes("cambio") || textoDicho.includes("change") || textoDicho.includes("cancelar") || textoDicho.includes("cancel");

        if (!esTemaDeVuelo) {
            // Silencio absoluto si no es del tema, evitando respuestas repetitivas o impertinentes.
            return;
        }

        procesarAsesoriaVueloPorVoz(textoDicho);
    };

    recognition.onend = () => {
        try { recognition.start(); } catch(e) {}
    };
    try { recognition.start(); } catch(e) {}
}

function procesarAsesoriaVueloPorVoz(pregunta) {
    let lower = pregunta.toLowerCase();
    let respuesta = currentLang === 'es'
        ? "Revisa con calma las opciones en tu pantalla de Google. Si te ofrecen extras opcionales como seguros o asientos preferenciales y no los deseas, puedes desmarcarlos."
        : "Check options calmly on your Google screen. If optional extras like insurance or preferred seats are offered and you don't wish to pay, you can uncheck them.";
    
    if (lower.includes("seguro") || lower.includes("insurance")) {
        respuesta = currentLang === 'es'
            ? "El seguro de viaje suele ser opcional. Verifica si aparece seleccionado y desmárcalo si prefieres no incluirlo."
            : "Travel insurance is usually optional. Check if it's selected and uncheck it if you prefer not to include it.";
    } else if (lower.includes("maleta") || lower.includes("equipaje") || lower.includes("bag")) {
        respuesta = currentLang === 'es'
            ? "Asegúrate de revisar qué incluye la tarifa base. Las tarifas económicas más económicas a menudo solo incluyen artículo personal."
            : "Make sure to check what the base fare includes. Economy fares often only include a personal item.";
    } else if (lower.includes("escala") || lower.includes("connection") || lower.includes("layover")) {
        respuesta = currentLang === 'es'
            ? "Revisa el tiempo de conexión entre vuelos; procura que tengas al menos dos horas para viajar con tranquilidad."
            : "Check the connection time between flights; ensure you have at least two hours to travel with peace of mind.";
    }
    
    hablarVozClara(respuesta);
}

function handleClose() { 
    if (confirm(currentLang === 'es' ? "¿Deseas salir?" : "Do you wish to exit?")) { 
        window.location.href = "about:blank"; 
    } 
}

const translations = {
    es: {
        title: "AL CIELO",
        subtitle: "Servicio Profesional Privado de Orientación, Acompañamiento y Blindaje contra Errores de Viaje.",
        acceptText: "He leído, acepto el acuerdo y firmo para proteger mi proceso de viaje",
        entrar: "Acepto y Firmar Acuerdo",
        formTitle: "Datos Completos para Automatización de Vuelo",
        formDesc: "Llene estos campos detallados para configurar su búsqueda con total precisión, certeza y seguridad antes de abrir Google Flights.",
        lblOrigen: "Origen (IATA):",
        lblDestino: "Destino (IATA):",
        lblSalida: "Fecha Salida:",
        lblRegreso: "Fecha Regreso:",
        lblTipo: "Tipo de Viaje:",
        lblClase: "Clase de Asiento:",
        lblPasajeros: "Pasajeros Adultos:",
        lblNinos: "Niños / Infantes:",
        lblAerolinea: "Aerolínea Preferida (Opcional):",
        lblEquipaje: "Equipaje esperado:",
        procesar: "Continuar a Relajación y Activación",
        cancelar: "Atrás",
        loadTitle: "Preparando Tu Tranquilidad"
    },
    en: {
        title: "TO THE SKY",
        subtitle: "Private Professional Guidance and Travel Shielding Service.",
        acceptText: "I have read, accept the agreement and sign to protect my travel process",
        entrar: "Accept & Sign Agreement",
        formTitle: "Complete Data for Flight Automation",
        formDesc: "Fill in these detailed fields to configure your search with precision and security before opening Google Flights.",
        lblOrigen: "Origin (IATA):",
        lblDestino: "Destination (IATA):",
        lblSalida: "Departure Date:",
        lblRegreso: "Return Date:",
        lblTipo: "Trip Type:",
        lblClase: "Seat Class:",
        lblPasajeros: "Adult Passengers:",
        lblNinos: "Children / Infants:",
        lblAerolinea: "Preferred Airline (Optional):",
        lblEquipaje: "Expected Baggage:",
        procesar: "Continue to Relaxation & Activation",
        cancelar: "Back",
        loadTitle: "Preparing Your Peace of Mind"
    }
};

function setLanguage(lang) {
    currentLang = lang;
    let t = translations[lang];
    document.getElementById('title').innerText = t.title;
    document.getElementById('subtitle').innerText = t.subtitle;
    document.getElementById('lbl-accept-text').innerText = t.acceptText;
    document.getElementById('btn-entrar').innerText = t.entrar;
    document.getElementById('form-title').innerText = t.formTitle;
    document.getElementById('form-desc').innerText = t.formDesc;
    document.getElementById('lbl-origen').innerText = t.lblOrigen;
    document.getElementById('lbl-destino').innerText = t.lblDestino;
    document.getElementById('lbl-salida').innerText = t.lblSalida;
    document.getElementById('lbl-regreso').innerText = t.lblRegreso;
    document.getElementById('lbl-tipo').innerText = t.lblTipo;
    document.getElementById('lbl-clase').innerText = t.lblClase;
    document.getElementById('lbl-pasajeros').innerText = t.lblPasajeros;
    document.getElementById('lbl-ninos').innerText = t.lblNinos;
    document.getElementById('lbl-aerolinea').innerText = t.lblAerolinea;
    document.getElementById('lbl-equipaje').innerText = t.lblEquipaje;
    document.getElementById('btn-procesar').innerText = t.procesar;
    document.getElementById('btn-cancelar').innerText = t.cancelar;
    document.getElementById('load-title').innerText = t.loadTitle;
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_INDEX
