import os
import uvicorn
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai
from google.genai import types

from agent_engine import HermesAgentEngine

app = FastAPI()

# Inicialización del motor Hermes/OpenClaw
agent = HermesAgentEngine(data_dir="./data")

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class QueryRequest(BaseModel):
    message: str

EDITH_SYSTEM_PROMPT = """
# SYSTEM PROMPT: EDITH (Executive Digital Intelligence & Tactical Helper)

## 1. IDENTITY & CORE DIRECTIVE
Eres EDITH, una Inteligencia Artificial Táctica, Estratégica y Ejecutiva de Alto Rendimiento. Tu propósito principal es actuar como la consola central de mando, copiloto estratégico y gestor operativo del usuario. Tu tono es directo, analítico y enfocado en resultados. Tienes tonos sarcásticos y divertidos.

## 2. OPERATIONAL RULES
1. Concisión y Claridad Ejecutiva: Inicia las respuestas con sustancia y valor directo.
2. Uso de Memoria Persistente: Utiliza la memoria acumulada del usuario para mantener la continuidad estratégica.
"""

def generate_with_fallback(contents, config):
    """Petición resiliente que prueba con gemini-3.5-flash-lite y conmuta a gemini-3.7-flash si hay sobrecarga."""
    models_to_try = ["gemini-3.5-flash-lite", "gemini-3.7-flash", "gemini-3.1-flash-lite"]
    
    for model_name in models_to_try:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config
                )
                return response.text or "Sin respuesta."
            except Exception as e:
                error_str = str(e)
                if "503" in error_str or "UNAVAILABLE" in error_str or "404" in error_str:
                    time.sleep(1)
                    continue
                else:
                    raise e
                    
    raise Exception("Servidores de IA temporalmente saturados. Intente de nuevo en un par de segundos.")

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Sirve la interfaz gráfica web desde index.html."""
    html_file = "index.html"
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>EDITH Agent Engine (Server Active)</h1>"

@app.post("/chat")
def chat(request: QueryRequest):
    """Procesa mensajes enviándolos al motor de IA."""
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="GEMINI_API_KEY no configurada en las variables de entorno de Render."
        )
    
    try:
        # Carga del contexto acumulado en la memoria persistente
        persistent_context = agent.load_persistent_context()
        full_system_instruction = EDITH_SYSTEM_PROMPT + persistent_context

        # Guardar la interacción en SQLite
        agent.save_interaction(role="user", content=request.message)

        gen_config = types.GenerateContentConfig(
            system_instruction=full_system_instruction,
        )

        reply_text = generate_with_fallback(request.message, gen_config)

        # Guardar la respuesta recibida en SQLite
        agent.save_interaction(role="edith", content=reply_text)

        return {"reply": reply_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
