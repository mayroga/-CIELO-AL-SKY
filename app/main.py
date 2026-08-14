import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_INDEX = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AL CIELO</title>
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
    </style>
</head>
<body>

<div class="main-container">
    <div id="language-controls" style="text-align: right; margin-bottom: 10px;">
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
            <button id="btn-cerrar" class="btn-danger" onclick="handleClose()">Cerrar</button>
        </div>
    </div>

    <!-- VISTA 2: FORMULARIO DE DATOS -->
    <div id="view-form" class="hidden">
        <h2 id="form-title">Datos Completos para Automatización de Vuelo</h2>
        <p id="form-desc" style="color: #666; font-size: 13px;">Llene estos campos para configurar su búsqueda en Google de manera limpia y sin interferencias.</p>
        
        <div style="text-align: left; display: inline-block; width: 100%; font-size: 13px;">
            <div style="display: flex; gap: 10px;">
                <div style="flex: 1;"><label style="font-weight: bold; color: #004080;">Origen (IATA):</label><input type="text" id="origen" placeholder="Ej: MIA"></div>
                <div style="flex: 1;"><label style="font-weight: bold; color: #004080;">Destino (IATA):</label><input type="text" id="destino" placeholder="Ej: MAD"></div>
            </div>

            <div style="display: flex; gap: 10px; margin-top: 8px;">
                <div style="flex: 1;"><label style="font-weight: bold; color: #004080;">Fecha Salida:</label><input type="date" id="fecha_salida"></div>
                <div style="flex: 1;"><label style="font-weight: bold; color: #004080;">Fecha Regreso:</label><input type="date" id="fecha_regreso"></div>
            </div>
        </div>

        <div id="error-box" class="error-message hidden"></div>
        
        <div style="margin-top: 20px;">
            <button class="btn-primary" onclick="prepararConexionRespiratoria()">Continuar a Activación</button>
            <button class="btn-danger" onclick="switchView('view-home')">Atrás</button>
        </div>
    </div>

    <!-- VISTA 3: RELAJACIÓN Y APERTURA LIMPIA DE GOOGLE -->
    <div id="view-loading" class="hidden">
        <h2 id="load-title">Preparando Tu Tranquilidad</h2>
        <p style="color: #555; font-size: 13px; line-height: 1.4;">Inhala profundo. Abriremos Google Flights de forma limpia y directa, manteniendo el audio por detrás para guiarte en lo que necesites.</p>
        
        <div id="breathing-circle"><span id="breath-txt">Inhala calma</span></div>
        
        <div style="background: #e8f4fd; border: 1px solid #bbe1fa; padding: 10px; border-radius: 6px; font-size: 12px; color: #004080; margin: 10px 0; text-align: left; line-height: 1.4;">
            🎙️ <strong>ASISTENCIA DE VOZ EN SEGUNDO PLANO:</strong> Al abrirse Google, la pantalla quedará 100% limpia y original. El micrófono te escuchará de fondo: di <em>"Apágate", "Pausa", "Silencio"</em> para detener la voz, o <em>"Enciéndete", "Habla"</em> para reactivarla en cualquier momento.
        </div>

        <div style="margin-top: 15px;">
            <button class="btn-success" onclick="abrirGooglePuroYActivarVoz()">✈️ ABRIR GOOGLE LIMPIO Y ACTIVAR VOZ DE FONDO</button>
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
    "10. Recuerda que puedes decir 'Apágate' o 'Enciéndete' por voz cuando quieras."
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
    "10. Remember you can say 'Turn off' or 'Turn on' by voice."
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
    hablarVozClara(currentLang === 'es' ? "Por favor completa los datos de tu viaje." : "Please fill in your travel data.");
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
    let errBox = document.getElementById('error-box');

    if (!org || !dest) {
        let msg = currentLang === 'es' ? "Por favor ingresa origen y destino." : "Please enter origin and destination.";
        errBox.innerText = msg;
        errBox.classList.remove('hidden');
        hablarVozClara(msg);
        return;
    }
    errBox.classList.add('hidden');
    
    let queryParams = `flights from ${org.toUpperCase().substring(0,3)} to ${dest.toUpperCase().substring(0,3)}`;
    if (depDate) queryParams += ` on ${depDate}`;
    if (retDate) queryParams += ` returning ${retDate}`;
    
    urlGoogleFlightsGlobal = `https://www.google.com/travel/flights?q=${encodeURIComponent(queryParams)}`;

    switchView('view-loading');
    iniciarCicloRespiratorioDinamico();
}

function abrirGooglePuroYActivarVoz() {
    if (breathInterval) {
        clearInterval(breathInterval);
        breathInterval = null;
    }
    
    // Abrir Google Flights en la misma pestaña o ventana principal de manera totalmente limpia y sin iframes
    window.location.href = urlGoogleFlightsGlobal;
}

function handleClose() { 
    if (confirm(currentLang === 'es' ? "¿Deseas salir?" : "Do you wish to exit?")) { 
        window.location.href = "about:blank"; 
    } 
}

function setLanguage(lang) {
    currentLang = lang;
}
</script> 
</body> 
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_INDEX
