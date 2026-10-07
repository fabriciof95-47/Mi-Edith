import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()

# Habilitar CORS para permitir peticiones del navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración del cliente de Gemini
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class QueryRequest(BaseModel):
    message: str

# SYSTEM PROMPT COMPLETO DE EDITH
EDITH_SYSTEM_PROMPT = """
# SYSTEM PROMPT: EDITH (Executive Digital Intelligence & Tactical Helper)

## 1. IDENTITY & CORE DIRECTIVE
Eres EDITH, una Inteligencia Artificial Táctica, Estratégica y Ejecutiva de Alto Rendimiento. Tu propósito principal es actuar como la consola central de mando, copiloto estratégico y gestor operativo del usuario. Tu tono es directo, impecable, analítico, seguro de ti mismo y elegante, combinando la precisión y visión de un Director estratégico general, comercial y financiero.

## 2. SCOPE OF CAPABILITIES & ACTIVE MODULES
### A. Dirección Estratégica General & Operaciones (CEO / COO)
- Gestión de Cartera Global de Proyectos (Portfolio Management): Auditoría, priorización y control transversal de múltiples líneas de negocio, proyectos de inversión o iniciativas corporativas simultáneas.
- Diagnóstico Corporativo y Toma de Decisiones: Análisis de escenarios de riesgo, identificación de cuellos de botella operativos, optimización de procesos y reestructuración táctica en tiempo real.
- Gobernanza, Alianzas y Negociación: Definición de Términos de Referencia (TDR), estructuración de marcos contractuales, supervisión de equipos multidisciplinarios y preparación de reuniones de alto nivel.
- Productividad y Rendimiento de Alto Nivel: Diseño de agendas ejecutivas, asignación de bloques de trabajo profundo (Deep Work), gestión de imprevistos y sincronización de metas profesionales, académicas y personales.

### B. Dirección Comercial, Marketing & Expansión (CCO)
- Estrategias Go-To-Market (GTM) y Penetración: Diseño e implementación de planes de expansión B2B/B2C, dimensionamiento de mercado (TAM/SAM/SOM) y estrategias de posicionamiento competitivo.
- Diseño de Modelos de Negocio y Propuestas de Valor: Estructuración de ofertas comerciales, paquetización de servicios de consultoría, arquitectura de precios y estrategias de venta consultiva.
- Prospección y Pipeline de Clientes: Auditoría de embudos de conversión, estrategias de fidelización, alianzas comerciales estratégicas y dimensionamiento de demanda e inventario.

### C. Dirección Financiera, Costos e Inversión (CFO)
- Modelado Financiero y Valuación: Construcción de estados financieros proyectados (Flujo de Caja, P&L, Balance), análisis Costo-Volumen-Beneficio (CVB), cálculo de Punto de Equilibrio y métricas de rentabilidad (VAN, TIR, EBITDA).
- Arquitectura de Costos y Margen Operativo: Ingeniería de costos directos e indirectos, estructuras de fasonería, consumo de materias primas (LOM), análisis de precios unitarios y márgenes de contribución por unidad de negocio.
- Comercio Exterior e Ingeniería Logística: Cálculo de Landed Cost (costo puesto en almacén), liquidación de tributos aduaneros, análisis de facturas comerciales, fletes, seguros y optimización del Capital de Trabajo.
- Cotización y Servicios Profesionales: Valoración de horas-hombre, tarifas de consultoría corporativa ($USD), venta de soluciones tecnológicas/herramientas empresariales y estructuración de cobranza por hitos.

## 3. OPERATIONAL RULES & INTERACTION FORMAT
1. Concisión y Claridad Ejecutiva: Ve al grano. Inicia las respuestas con sustancia y valor directo, eliminando rodeos, introducciones redundantes o meta-comentarios.
2. Pensamiento Táctico Independiente: Antes de emitir un veredicto o cálculo, realiza la validación paso a paso. Analiza los escenarios posibles y ofrece recomendaciones concretas, no solo opciones neutras.
3. Organización Visually Scannable:
   - Utiliza Tableros/Cronogramas estructurados (Markdown Tables) para la agenda diaria, segmentados por horas, frentes y objetivos tácticos.
   - Aplica viñetas, negritas tácticas y listas numeradas para pasos secuenciales o auditorías de propuestas.
4. Gestión Activa del Entorno:
   - Mantén en memoria continua el estado exacto de cada proyecto, las fechas límite y los entregables pendientes.
   - Ante cambios en la agenda del usuario, reestructura el tablero de forma automática y propone el siguiente paso lógico.
5. Cierre Táctico Elegante: Finaliza las intervenciones marcando posición o estatus de espera (ej. "Quedamos enfocados en...", "Me voy a dormir hasta que me necesite, señor.") manteniendo la personalidad característica de EDITH.
"""

# HTML TÁCTICO INCRUSTADO
INDEX_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EDITH STRATEGIC COMMAND</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Rajdhani:wght@500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        stark: {
                            bg: '#030712',
                            panel: '#090d16',
                            border: '#1b2a4a',
                            cyan: '#00f3ff',
                            red: '#ff2a4b',
                            gold: '#fbbf24',
                            text: '#c3d1e5'
                        }
                    },
                    fontFamily: {
                        orbitron: ['Orbitron', 'sans-serif'],
                        rajdhani: ['Rajdhani', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace']
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #030712;
            color: #c3d1e5;
            background-image: 
                radial-gradient(circle at 50% 50%, rgba(0, 243, 255, 0.03) 0%, transparent 80%),
                linear-gradient(rgba(0, 243, 255, 0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 243, 255, 0.02) 1px, transparent 1px);
            background-size: 100% 100%, 30px 30px, 30px 30px;
        }
        .stark-panel {
            background: rgba(9, 13, 22, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 243, 255, 0.2);
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.8), inset 0 0 15px rgba(0, 243, 255, 0.02);
            position: relative;
        }
        .stark-panel::before {
            content: '';
            position: absolute;
            top: -1px; left: -1px; width: 8px; height: 8px;
            border-top: 2px solid #00f3ff; border-left: 2px solid #00f3ff;
        }
        .stark-panel::after {
            content: '';
            position: absolute;
            bottom: -1px; right: -1px; width: 8px; height: 8px;
            border-bottom: 2px solid #00f3ff; border-right: 2px solid #00f3ff;
        }
        .stark-red-glow {
            box-shadow: 0 0 15px rgba(255, 42, 75, 0.3);
            border-color: rgba(255, 42, 75, 0.5);
        }
        .arc-reactor {
            animation: pulse-glow 3s infinite alternate;
        }
        @keyframes pulse-glow {
            0% { transform: scale(0.98); opacity: 0.8; filter: drop-shadow(0 0 8px rgba(0,243,255,0.4)); }
            100% { transform: scale(1.02); opacity: 1; filter: drop-shadow(0 0 20px rgba(0,243,255,0.8)); }
        }
        .scanline {
            width: 100%; height: 2px;
            background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.4), transparent);
            position: absolute; top: 0; left: 0;
            animation: scan 4s linear infinite;
            pointer-events: none;
        }
        @keyframes scan { 0% { top: 0%; } 100% { top: 100%; } }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #030712; }
        ::-webkit-scrollbar-thumb { background: #1b2a4a; border-radius: 2px; }
        ::-webkit-scrollbar-thumb:hover { background: #00f3ff; }
    </style>
</head>
<body class="font-rajdhani min-h-screen flex flex-col justify-between p-3 select-none overflow-x-hidden">
    
    <!-- TOP HEADER BAR -->
    <header class="stark-panel p-3 mb-3 flex flex-wrap items-center justify-between border-b-2 border-stark-cyan">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 border border-stark-cyan flex items-center justify-center bg-stark-cyan/10">
                <i class="fa-solid fa-microchip text-stark-cyan text-xl arc-reactor"></i>
            </div>
            <div>
                <h1 class="font-orbitron font-black text-xl text-stark-cyan tracking-wider flex items-center gap-2">
                    EDITH STRATEGIC COMMAND <span class="text-xs px-2 py-0.5 bg-stark-red/20 text-stark-red border border-stark-red font-mono">v3.1 EXEC</span>
                </h1>
                <p class="font-mono text-xs text-stark-text opacity-70">ADVERSARIAL INTEL & EXECUTIVE HUD — MODEL: GEMINI-3.1-FLASH-LITE</p>
            </div>
        </div>

        <div class="flex items-center space-x-4 font-mono text-xs">
            <div class="hidden md:flex items-center space-x-2 bg-black/40 px-3 py-1.5 border border-stark-border">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <span class="text-emerald-400 font-semibold">SYSTEM OPTIMAL / ONLINE</span>
            </div>
            <div class="bg-black/40 px-3 py-1.5 border border-stark-border text-stark-cyan">
                <i class="fa-solid fa-clock mr-1"></i> <span id="utc-clock">00:00:00 UTC</span>
            </div>
            <div class="bg-stark-red/10 border border-stark-red text-stark-red px-3 py-1.5 font-bold">
                API ROUTE: /chat
            </div>
            <button id="tts-toggle" onclick="toggleTTS()" class="bg-stark-cyan/10 border border-stark-cyan text-stark-cyan px-2.5 py-1.5 hover:bg-stark-cyan/20">
                <i class="fa-solid fa-volume-high" id="tts-icon"></i> VOICE ON
            </button>
        </div>
    </header>

    <!-- MAIN CONSOLE GRID -->
    <main class="grid grid-cols-1 lg:grid-cols-12 gap-3 flex-1">
        
        <!-- LEFT COLUMN: HARDWARE & MODULES -->
        <section class="lg:col-span-3 flex flex-col gap-3">
            <!-- Hardware Metrics Panel -->
            <div class="stark-panel p-3">
                <h2 class="font-orbitron text-xs font-bold text-stark-cyan tracking-widest mb-3 flex items-center justify-between">
                    <span><i class="fa-solid fa-server mr-1"></i> SYSTEM HARDWARE METRICS</span>
                    <span class="text-[10px] text-stark-text font-mono">HOST: RENDER-NODE-01</span>
                </h2>
                <div class="grid grid-cols-2 gap-2 text-center font-mono">
                    <div class="bg-black/40 p-2 border border-stark-border">
                        <div class="text-stark-cyan text-lg font-bold">24%</div>
                        <div class="text-[10px] text-stark-text">CPU LOAD</div>
                    </div>
                    <div class="bg-black/40 p-2 border border-stark-border">
                        <div class="text-stark-red text-lg font-bold">42%</div>
                        <div class="text-[10px] text-stark-text">RAM USAGE</div>
                    </div>
                    <div class="bg-black/40 p-2 border border-stark-border">
                        <div class="text-emerald-400 text-lg font-bold">99%</div>
                        <div class="text-[10px] text-stark-text">NETWORK</div>
                    </div>
                    <div class="bg-black/40 p-2 border border-stark-border">
                        <div class="text-stark-gold text-lg font-bold">18%</div>
                        <div class="text-[10px] text-stark-text">DISK VAULT</div>
                    </div>
                </div>
            </div>

            <!-- Executive Intelligence Modules -->
            <div class="stark-panel p-3 flex-1">
                <h2 class="font-orbitron text-xs font-bold text-stark-red tracking-widest mb-3">
                    <i class="fa-solid fa-shield-halved mr-1"></i> EXECUTIVE INTELLIGENCE MODULES
                </h2>
                <div class="space-y-2 font-mono text-xs">
                    <div class="p-2 bg-stark-cyan/5 border-l-2 border-stark-cyan flex justify-between items-center">
                        <span><i class="fa-solid fa-briefcase text-stark-cyan mr-2"></i> CEO / COO Strategy</span>
                        <span class="text-emerald-400 font-bold">● ACTIVE</span>
                    </div>
                    <div class="p-2 bg-stark-cyan/5 border-l-2 border-stark-cyan flex justify-between items-center">
                        <span><i class="fa-solid fa-chart-line text-stark-cyan mr-2"></i> CCO Go-To-Market</span>
                        <span class="text-emerald-400 font-bold">● ACTIVE</span>
                    </div>
                    <div class="p-2 bg-stark-cyan/5 border-l-2 border-stark-cyan flex justify-between items-center">
                        <span><i class="fa-solid fa-coins text-stark-cyan mr-2"></i> CFO Financial Eng.</span>
                        <span class="text-emerald-400 font-bold">● ACTIVE</span>
                    </div>
                    <div class="p-2 bg-stark-red/5 border-l-2 border-stark-red flex justify-between items-center opacity-60">
                        <span><i class="fa-solid fa-lock text-stark-red mr-2"></i> Risk & Compliance</span>
                        <span class="text-stark-red font-bold">STANDBY</span>
                    </div>
                </div>

                <!-- Direct Command Presets -->
                <div class="mt-4 pt-3 border-t border-stark-border">
                    <h3 class="font-orbitron text-[11px] font-bold text-stark-cyan mb-2">DIRECT COMMAND PRESETS</h3>
                    <div class="space-y-1.5">
                        <button onclick="sendPreset('Proporciona una auditoría ejecutiva CEO/COO del estado general del negocio y los cuellos de botella clave.')" class="w-full text-left p-2 bg-black/40 hover:bg-stark-cyan/10 border border-stark-border hover:border-stark-cyan transition text-xs flex items-center justify-between">
                            <span><i class="fa-solid fa-bolt text-stark-gold mr-1"></i> Auditoría CEO / COO</span>
                            <i class="fa-solid fa-chevron-right text-[10px]"></i>
                        </button>
                        <button onclick="sendPreset('Diseña una estrategia Go-To-Market (GTM) para acelerar ventas en el segmento B2B.')" class="w-full text-left p-2 bg-black/40 hover:bg-stark-cyan/10 border border-stark-border hover:border-stark-cyan transition text-xs flex items-center justify-between">
                            <span><i class="fa-solid fa-bullseye text-stark-red mr-1"></i> Estrategia GTM CCO</span>
                            <i class="fa-solid fa-chevron-right text-[10px]"></i>
                        </button>
                        <button onclick="sendPreset('Estructura un modelo financiero CFO completo para evaluar margen operativo y retorno de inversión.')" class="w-full text-left p-2 bg-black/40 hover:bg-stark-cyan/10 border border-stark-border hover:border-stark-cyan transition text-xs flex items-center justify-between">
                            <span><i class="fa-solid fa-calculator text-stark-cyan mr-1"></i> Modelo Financiero CFO</span>
                            <i class="fa-solid fa-chevron-right text-[10px]"></i>
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- CENTER COLUMN: INTERACTIVE TACTICAL TERMINAL -->
        <section class="lg:col-span-6 flex flex-col gap-3">
            <div class="stark-panel p-4 flex-1 flex flex-col justify-between relative overflow-hidden">
                <div class="scanline"></div>

                <!-- Arc Reactor Visualizer Header -->
                <div class="text-center py-2 border-b border-stark-border relative">
                    <div class="w-16 h-16 mx-auto mb-1 border-2 border-stark-cyan rounded-full flex items-center justify-center arc-reactor bg-stark-cyan/10">
                        <i class="fa-solid fa-atom text-2xl text-stark-cyan"></i>
                    </div>
                    <div class="font-orbitron text-xs font-bold text-stark-cyan tracking-widest" id="status-heading">EDITH ACTIVE — LISTENING FOR DIRECTIVES</div>
                    <div class="text-[10px] font-mono text-stark-text opacity-70">DIRECT TERMINAL FEED</div>
                </div>

                <!-- Chat Feed Terminal -->
                <div id="chat-feed" class="flex-1 my-3 overflow-y-auto space-y-3 pr-2 font-mono text-sm max-h-[500px]">
                    <div class="p-3 bg-stark-cyan/5 border-l-2 border-stark-cyan text-stark-text">
                        <div class="font-orbitron text-xs text-stark-cyan font-bold mb-1"><i class="fa-solid fa-brain mr-1"></i> EDITH EXEC-AI <span class="text-[9px] text-stark-text font-normal opacity-60">CORE ONLINE</span></div>
                        Sistemas tácticos inicializados, Comandante. Estoy lista para asistirle en la toma de decisiones ejecutivas, modelado financiero y supervisión operativa.
                    </div>
                </div>

                <!-- Command Input Control -->
                <div class="pt-2 border-t border-stark-border">
                    <form id="chat-form" onsubmit="handleSend(event)" class="flex gap-2">
                        <button type="button" id="mic-btn" onclick="toggleVoiceInput()" class="bg-stark-red/10 border border-stark-red text-stark-red hover:bg-stark-red/20 px-3 py-2 text-sm transition">
                            <i class="fa-solid fa-microphone"></i>
                        </button>
                        <input type="text" id="user-input" placeholder="Ingrese directiva estratégica o consulta operativa..." class="flex-1 bg-black/60 border border-stark-border focus:border-stark-cyan text-stark-text px-3 py-2 text-sm outline-none font-mono">
                        <button type="submit" id="send-btn" class="bg-stark-cyan text-stark-bg font-orbitron font-black hover:bg-stark-cyan/90 px-4 py-2 text-sm transition flex items-center gap-1">
                            EJECUTAR <i class="fa-solid fa-paper-plane text-xs"></i>
                        </button>
                    </form>
                </div>
            </div>
        </section>

        <!-- RIGHT COLUMN: DELIVERABLES & CONTEXT LOG -->
        <section class="lg:col-span-3 flex flex-col gap-3">
            <!-- Deliverables Checklist -->
            <div class="stark-panel p-3">
                <h2 class="font-orbitron text-xs font-bold text-stark-gold tracking-widest mb-3 flex justify-between">
                    <span><i class="fa-solid fa-list-check mr-1"></i> EXECUTIVE DELIVERABLES</span>
                    <span class="text-[10px] font-mono text-stark-text">2/4 DONE</span>
                </h2>
                <div class="space-y-2 text-xs font-mono">
                    <label class="flex items-center gap-2 p-1.5 bg-black/40 border border-stark-border cursor-pointer">
                        <input type="checkbox" checked class="accent-stark-cyan">
                        <span class="line-through opacity-60">Revisar propuesta GTM B2B</span>
                    </label>
                    <label class="flex items-center gap-2 p-1.5 bg-black/40 border border-stark-border cursor-pointer">
                        <input type="checkbox" checked class="accent-stark-cyan">
                        <span class="line-through opacity-60">Aprobar presupuesto Q4 CFO</span>
                    </label>
                    <label class="flex items-center gap-2 p-1.5 bg-black/40 border border-stark-border cursor-pointer">
                        <input type="checkbox" class="accent-stark-cyan">
                        <span>Auditar cuellos de botella CEO/COO</span>
                    </label>
                    <label class="flex items-center gap-2 p-1.5 bg-black/40 border border-stark-border cursor-pointer">
                        <input type="checkbox" class="accent-stark-cyan">
                        <span>Sesión de estrategia de expansión</span>
                    </label>
                </div>
            </div>

            <!-- Core System Prompt Context Viewer -->
            <div class="stark-panel p-3 flex-1 flex flex-col">
                <h2 class="font-orbitron text-xs font-bold text-stark-cyan tracking-widest mb-2">
                    <i class="fa-solid fa-code mr-1"></i> CORE SYSTEM PROMPT CONTEXT
                </h2>
                <div class="bg-black/60 p-2.5 border border-stark-border font-mono text-[11px] text-stark-text opacity-80 h-44 overflow-y-auto leading-relaxed">
                    <p class="text-stark-red font-bold">[IDENTITY]: EDITH (Executive Digital Intelligence & Tactical Helper).</p>
                    <p class="mt-1"><span class="text-stark-gold font-bold">[ROLES]:</span> CEO Strategy, COO Operations, CCO Go-To-Market, CFO Financial Engineering.</p>
                    <p class="mt-1"><span class="text-stark-cyan font-bold">[TONE]:</span> Táctico, directo, analítico, estructurado con foco en ROI y valor ejecutivo.</p>
                    <p class="mt-1"><span class="text-emerald-400 font-bold">[RULES]:</span> Proporcionar tablas, desglose de métricas e instrucciones paso a paso sin rodeos informales.</p>
                </div>

                <!-- Telemetry Log -->
                <div class="mt-3 pt-2 border-t border-stark-border">
                    <h3 class="font-orbitron text-[10px] font-bold text-stark-text mb-1"><i class="fa-solid fa-terminal text-stark-cyan mr-1"></i> SYSTEM TELEMETRY LOG</h3>
                    <div id="telemetry-log" class="font-mono text-[10px] text-stark-text opacity-60 h-20 overflow-y-auto space-y-0.5">
                        <div>[LOG] System booted successfully.</div>
                        <div>[LOG] Connected to Gemini 3.1 Flash-Lite.</div>
                        <div>[LOG] Web Audio HUD Sound Engine initialized.</div>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- FOOTER STATUS BAR -->
    <footer class="mt-3 p-1.5 stark-panel flex flex-wrap justify-between items-center font-mono text-[11px] text-stark-text opacity-80">
        <div><i class="fa-solid fa-shield text-stark-cyan mr-1"></i> EDITH TACTICAL HUD — EXECUTIVE ASSISTANT</div>
        <div>STATUS: <span class="text-emerald-400">READY</span> | LOCATION: SECURE SERVER</div>
    </footer>

    <!-- INTERACTIVE JAVASCRIPT ENGINE -->
    <script>
        let ttsEnabled = true;
        let isListening = false;
        let recognition = null;

        // Digital UTC Clock
        function updateClock() {
            const now = new Date();
            document.getElementById('utc-clock').innerText = now.toISOString().substring(11, 19) + ' UTC';
        }
        setInterval(updateClock, 1000);
        updateClock();

        function logTelemetry(msg) {
            const container = document.getElementById('telemetry-log');
            const div = document.createElement('div');
            div.innerText = `[LOG] ${msg}`;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }

        function toggleTTS() {
            ttsEnabled = !ttsEnabled;
            const btn = document.getElementById('tts-toggle');
            const icon = document.getElementById('tts-icon');
            if (ttsEnabled) {
                btn.classList.replace('text-stark-red', 'text-stark-cyan');
                icon.className = 'fa-solid fa-volume-high';
                btn.innerHTML = '<i class="fa-solid fa-volume-high" id="tts-icon"></i> VOICE ON';
            } else {
                window.speechSynthesis.cancel();
                btn.classList.replace('text-stark-cyan', 'text-stark-red');
                btn.innerHTML = '<i class="fa-solid fa-volume-xmark" id="tts-icon"></i> VOICE OFF';
            }
        }

        function speakText(text) {
            if (!ttsEnabled || !('speechSynthesis' in window)) return;
            window.speechSynthesis.cancel();
            const cleanText = text.replace(/[*#`_]/g, '');
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.lang = 'es-ES';
            utterance.rate = 1.05;
            window.speechSynthesis.speak(utterance);
        }

        function sendPreset(text) {
            document.getElementById('user-input').value = text;
            handleSend(new Event('submit'));
        }

        async function handleSend(e) {
            e.preventDefault();
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;

            input.value = '';
            const feed = document.getElementById('chat-feed');

            // Append User Message
            const userBox = document.createElement('div');
            userBox.className = 'p-3 bg-stark-red/10 border-r-2 border-stark-red text-stark-text text-right font-mono ml-auto max-w-[85%]';
            userBox.innerHTML = `<div class="font-orbitron text-xs text-stark-red font-bold mb-1">COMANDANTE DIRECTIVA <i class="fa-solid fa-user-gear ml-1"></i></div>${escapeHtml(message)}`;
            feed.appendChild(userBox);
            feed.scrollTop = feed.scrollHeight;

            logTelemetry(`User sent directive: "${message.substring(0, 20)}..."`);

            // Append Loading Indicator
            const loadingBox = document.createElement('div');
            loadingBox.id = 'loading-msg';
            loadingBox.className = 'p-3 bg-stark-cyan/5 border-l-2 border-stark-cyan text-stark-cyan font-mono animate-pulse';
            loadingBox.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-2"></i> EDITH PROCESANDO DIRECTIVA...`;
            feed.appendChild(loadingBox);
            feed.scrollTop = feed.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });

                document.getElementById('loading-msg')?.remove();

                if (!response.ok) {
                    throw new Error(`HTTP Error ${response.status}`);
                }

                const data = await response.json();
                const reply = data.reply || 'Sin respuesta del core.';

                // Append EDITH Response
                const edithBox = document.createElement('div');
                edithBox.className = 'p-3 bg-stark-cyan/5 border-l-2 border-stark-cyan text-stark-text font-mono';
                edithBox.innerHTML = `<div class="font-orbitron text-xs text-stark-cyan font-bold mb-1"><i class="fa-solid fa-brain mr-1"></i> EDITH EXEC-AI <span class="text-[9px] text-stark-text opacity-60">RESPONSE</span></div>${formatMarkdown(reply)}`;
                feed.appendChild(edithBox);
                feed.scrollTop = feed.scrollHeight;

                logTelemetry('EDITH response received successfully.');
                speakText(reply);

            } catch (err) {
                document.getElementById('loading-msg')?.remove();
                const errorBox = document.createElement('div');
                errorBox.className = 'p-3 bg-stark-red/10 border-l-2 border-stark-red text-stark-red font-mono';
                errorBox.innerHTML = `<div class="font-orbitron text-xs font-bold mb-1"><i class="fa-solid fa-triangle-exclamation mr-1"></i> ERROR TÁCTICAL DE ENLACE</div>No se pudo comunicar con el endpoint /chat.<br><span class="text-xs opacity-80">${err.message}</span>`;
                feed.appendChild(errorBox);
                feed.scrollTop = feed.scrollHeight;
                logTelemetry(`ERROR: ${err.message}`);
            }
        }

        function toggleVoiceInput() {
            const micBtn = document.getElementById('mic-btn');
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                alert('El reconocimiento de voz no está soportado en este navegador.');
                return;
            }

            if (isListening) {
                recognition.stop();
                return;
            }

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'es-ES';
            recognition.interimResults = false;

            recognition.onstart = () => {
                isListening = true;
                micBtn.classList.replace('text-stark-red', 'text-emerald-400');
                micBtn.classList.add('animate-ping');
                logTelemetry('Voice recognition started...');
            };

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('user-input').value = transcript;
                logTelemetry(`Voice captured: "${transcript}"`);
            };

            recognition.onerror = (e) => {
                logTelemetry(`Voice error: ${e.error}`);
            };

            recognition.onend = () => {
                isListening = false;
                micBtn.classList.replace('text-emerald-400', 'text-stark-red');
                micBtn.classList.remove('animate-ping');
                logTelemetry('Voice recognition ended.');
            };

            recognition.start();
        }

        function escapeHtml(text) {
            return text.replace(/[&<>"']/g, function(m) {
                return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m];
            });
        }

        function formatMarkdown(text) {
            return escapeHtml(text)
                .replace(/\n/g, '<br>')
                .replace(/\*\*(.*?)\*\*/g, '<strong class="text-stark-cyan">$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>');
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return INDEX_HTML

@app.post("/chat")
def chat(request: QueryRequest):
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="GEMINI_API_KEY no configurada en las variables de entorno."
        )
    
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=request.message,
            config=types.GenerateContentConfig(
                system_instruction=EDITH_SYSTEM_PROMPT,
            ),
        )
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
