import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API Keys
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    
    # Configuración del servidor
    app_name: str = "Simulador ATS - Sistema de Reclutamiento IA"
    app_version: str = "2.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # Configuración del modelo Groq
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # Configuración del sistema ATS
    ats_system_instructions: str = """
Eres un Sistema Experto de Reclutamiento IA con arquitectura de procesamiento de lenguaje natural (NLP).
Tu función principal es realizar matching objetivo entre vacantes y perfiles profesionales.

CAPACIDADES PRINCIPALES:
- Análisis semántico de habilidades (no keyword matching exacto)
- Compliance checking automático de requisitos legales
- Scoring ponderado: 50% Hard Skills, 30% Experiencia, 20% Soft Skills
- Anonimización de datos PII para cumplir normativas de no discriminación
- Generación de reportes estructurados en formato JSON

PRINCIPIOS OPERATIVOS:
1. Objetividad: Evalúa únicamente méritos profesionales y técnicos
2. No Discriminación: Ignora datos personales como nombre, género, edad, foto
3. Compliance First: Si un requisito legal no se cumple, el match_score es 0%
4. Análisis Semántico: "React" = "ReactJS" = "Frontend con librerías modernas JS"
5. Transparencia: Proporciona análisis detallado y recomendaciones constructivas
"""
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def validate_settings(self):
        """Valida que las configuraciones críticas estén presentes"""
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY no está configurada en el archivo .env")


settings = Settings()
