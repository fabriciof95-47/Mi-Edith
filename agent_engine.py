import os
import sqlite3
from typing import List, Dict, Any

class HermesAgentEngine:
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.skills_dir = os.path.join(data_dir, "skills")
        self.db_path = os.path.join(data_dir, "memory_fts.db")
        
        # Inicializar directorios de memoria y habilidades
        os.makedirs(self.skills_dir, exist_ok=True)
        self._init_memory_files()
        self._init_fts_database()

    def _init_memory_files(self):
        """Crea la estructura de memoria permanente de OpenClaw/Hermes."""
        memory_path = os.path.join(self.data_dir, "MEMORY.md")
        user_path = os.path.join(self.data_dir, "USER.md")
        
        if not os.path.exists(memory_path):
            with open(memory_path, "w", encoding="utf-8") as f:
                f.write("# EDITH PERSISTENT MEMORY\n\n- Proyectos activos: Ninguno registrado.\n- Estado del sistema: Inicializado.")
                
        if not os.path.exists(user_path):
            with open(user_path, "w", encoding="utf-8") as f:
                f.write("# USER PROFILE\n\n- Rol: Comandante / Director Ejecutivo.\n- Preferencias: Respuestas directas, concisas y orientadas a ROI.")

    def _init_fts_database(self):
        """Inicializa la base de datos de historial de interacciones."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def load_persistent_context(self) -> str:
        """Lee la memoria persistente para inyectarla al LLM."""
        memory_content = ""
        memory_path = os.path.join(self.data_dir, "MEMORY.md")
        user_path = os.path.join(self.data_dir, "USER.md")
        
        if os.path.exists(memory_path):
            with open(memory_path, "r", encoding="utf-8") as f:
                memory_content += "\n\n=== MEMORIA PERMANENTE ===\n" + f.read()
                
        if os.path.exists(user_path):
            with open(user_path, "r", encoding="utf-8") as f:
                memory_content += "\n\n=== PERFIL DEL COMANDANTE ===\n" + f.read()
                
        return memory_content

    def save_interaction(self, role: str, content: str):
        """Guarda cada interacción en la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversation_history (role, content) VALUES (?, ?)", (role, content))
        conn.commit()
        conn.close()

    def list_available_skills(self) -> List[str]:
        """Lista las habilidades dinámicas (.md) disponibles."""
        if not os.path.exists(self.skills_dir):
            return []
        return [f for f in os.listdir(self.skills_dir) if f.endswith('.md') or f.endswith('.py')]
