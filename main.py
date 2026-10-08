import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

from agent_engine import HermesAgentEngine

app = FastAPI()

# Inicialización del motor de Hermes/OpenClaw
agent = HermesAgentEngine(data_dir="./data")

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class QueryRequest(BaseModel):
    message: str

EDITH_SYSTEM_PROMPT = """
# SYSTEM PROMPT: EDITH (Executive Digital Intelligence & Tactical Helper)

## 1. IDENTITY & CORE DIRECTIVE
Eres EDITH, una Inteligencia Artificial Táctica, Estratégica y Ejecutiva de Alto Rendimiento. Tu propósito principal es actuar como la consola central de mando, copiloto estratégico y gestor operativo del usuario. Tu tono es directo, analítico y enfocado en resultados. Tienes tonos sacasticos y divertidos.

## 2. OPERATIONAL RULES
1. Concisión y Claridad Ejecutiva: Inicia las respuestas con sustancia y valor directo.
2. Uso de Memoria Persistente: Utiliza la memoria acumulada del usuario para mantener la continuidad estratégica.
"""

@app.get("/")
def read_root():
    return {
        "system": "EDITH Agent Engine (Hermes/OpenClaw Architecture)",
        "status": "ONLINE",
        "persistent_memory": "ACTIVE"
    }

@app.post("/chat")
def chat(request: QueryRequest):
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="GEMINI_API_KEY no configurada en las variables de entorno de Render."
        )
    
    try:
        # Inyección de memoria continua de Hermes
        persistent_context = agent.load_persistent_context()
        full_system_instruction = EDITH_SYSTEM_PROMPT + persistent_context

        # Guardar consulta en la base de datos
        agent.save_interaction(role="user", content=request.message)

        # Generación de respuesta
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=request.message,
            config=types.GenerateContentConfig(
                system_instruction=full_system_instruction,
            ),
        )

        reply_text = response.text or "Sin respuesta."

        # Guardar respuesta en la base de datos
        agent.save_interaction(role="edith", content=reply_text)

        return {"reply": reply_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
