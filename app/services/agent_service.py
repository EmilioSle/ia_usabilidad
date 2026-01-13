import json
import os
import warnings
from typing import Dict, Any
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.models.groq import GroqTools
from app.config import settings
from app.models.schemas import VacanteData, CandidatoData

# Suprimir advertencias de Pydantic sobre namespace 'model_'
warnings.filterwarnings("ignore", message=".*Field.*has conflict with protected namespace.*model_.*")


class AgentService:
    """Servicio para manejar la lógica del agente AGNO como Simulador ATS"""
    
    def __init__(self):
        """Inicializa el servicio del agente"""
        settings.validate_settings()
        
        # Configurar la API key de Groq como variable de entorno
        os.environ["GROQ_API_KEY"] = settings.groq_api_key
        
        # Crear el agente con el modelo de Groq especificado
        self.agent = Agent(
            model=Groq(id=settings.groq_model),
            instructions=[settings.ats_system_instructions],
            tools=[GroqTools()],
            markdown=False
        )
    
    def build_ats_prompt(self, vacante: VacanteData, candidato: CandidatoData) -> str:
        """
        Construye el prompt del Simulador ATS con análisis semántico
        
        Args:
            vacante: Datos de la vacante
            candidato: Datos del candidato
            
        Returns:
            Prompt estructurado para el análisis ATS
        """
        
        prompt = f"""
## SIMULADOR DE ATS - ANÁLISIS DE MATCHING

### ROL DEL SISTEMA:
Actúa como un Sistema Experto de Reclutamiento IA con arquitectura de procesamiento de lenguaje natural (NLP).
Tu función es realizar un matching objetivo entre una vacante y un perfil, simulando un pipeline de datos heterogéneos.

### INSTRUCCIONES DEL ALGORITMO (Paso a Paso):

#### 1. INGESTA Y PRE-PROCESAMIENTO (Simulado):
- Recibirás dos conjuntos de datos: "VACANTE" y "CANDIDATO"
- **Anonimización**: Ignora cualquier dato PII (Nombre, Género, Edad, Foto) para cumplir con normativa de No Discriminación
- **Evalúa solo méritos profesionales y técnicos**

#### 2. CAPA DE COMPLIANCE (Filtro Excluyente):
**REGLA CRÍTICA**: Si un requisito legal/excluyente NO se cumple, el match_score debe ser automáticamente 0% y estado RECHAZADO.
Verifica:
- Permiso de trabajo: {'✓ Requerido' if vacante.work_permit_required else '✗ No requerido'}
- Ubicación requerida: {vacante.location_required or 'No especificada'}
- Educación mínima: {vacante.education or 'No especificada'}

#### 3. MOTOR DE MATCHING (Análisis Vectorial Simulado):
**NO uses búsqueda exacta de palabras clave**. Usa análisis semántico:
- "React" = "ReactJS" = "Frontend con librerías modernas JS"
- "Python" = "Desarrollo en lenguajes de scripting" = "Backend con Python/Django"

**Compara:**
- **Hard Skills** (50%): Tecnologías, herramientas, idiomas técnicos
- **Experiencia** (30%): Años y relevancia del sector
- **Soft Skills/Culture Fit** (20%): Liderazgo, comunicación (inferidas del texto)

#### 4. GENERACIÓN DE OUTPUT:
Calcula un Score de Afinidad (0-100) y genera análisis JSON estructurado.

---

### DATOS DE LA VACANTE:
```json
{{
    "puesto": "{vacante.job_title}",
    "descripcion": "{vacante.job_description}",
    "hard_skills_requeridas": {json.dumps(vacante.hard_skills, ensure_ascii=False)},
    "soft_skills_deseadas": {json.dumps(vacante.soft_skills or [], ensure_ascii=False)},
    "años_experiencia": {vacante.years_experience},
    "educacion": "{vacante.education or 'No especificada'}",
    "idiomas": {json.dumps(vacante.languages or [], ensure_ascii=False)},
    "ubicacion_requerida": "{vacante.location_required or 'Flexible'}",
    "permiso_trabajo_requerido": {str(vacante.work_permit_required).lower()},
    "sector": "{vacante.sector or 'General'}"
}}
```

### DATOS DEL CANDIDATO:
```json
{{
    "cv_completo": "{candidato.cv_text}",
    "habilidades": {json.dumps(candidato.skills, ensure_ascii=False)},
    "años_experiencia": {candidato.years_experience},
    "educacion": "{candidato.education}",
    "idiomas": {json.dumps(candidato.languages, ensure_ascii=False)},
    "ubicacion_actual": "{candidato.location}",
    "tiene_permiso_trabajo": {str(candidato.has_work_permit).lower()},
    "experiencia_sector": "{candidato.sector_experience or 'No especificada'}",
    "info_adicional": "{candidato.additional_info or 'N/A'}"
}}
```

---

### FORMATO DE RESPUESTA REQUERIDO:
Debes responder EXCLUSIVAMENTE con un objeto JSON válido con esta estructura:

{{
    "match_score": <float 0-100>,
    "status": "<APROBADO|RECHAZADO|PENDIENTE>",
    "skill_analysis": {{
        "hard_skills_score": <float 0-100>,
        "soft_skills_score": <float 0-100>,
        "matched_skills": ["skill1", "skill2", ...],
        "missing_skills": ["skill1", "skill2", ...]
    }},
    "experience_score": <float 0-100>,
    "compliance_check": {{
        "has_work_permit": <true|false>,
        "location_match": <true|false>,
        "education_match": <true|false>
    }},
    "recommendations": ["recomendación 1", "recomendación 2", ...],
    "summary": "Resumen ejecutivo en 2-3 líneas",
    "detailed_analysis": "Análisis detallado completo del matching"
}}

**IMPORTANTE**: 
- Si compliance_check falla en algún punto crítico, match_score debe ser 0 y status debe ser RECHAZADO
- Usa análisis semántico, no matching exacto de palabras
- Sé objetivo y profesional en el análisis
"""
        return prompt
    
    def process_ats_matching(self, vacante: VacanteData, candidato: CandidatoData) -> Dict[str, Any]:
        """
        Procesa el matching ATS entre vacante y candidato
        
        Args:
            vacante: Datos de la vacante
            candidato: Datos del candidato
            
        Returns:
            Diccionario con el análisis completo del matching
        """
        # Construir el prompt del ATS
        prompt = self.build_ats_prompt(vacante, candidato)
        
        # Procesar con el agente
        response = self.agent.run(prompt)
        
        # Extraer el contenido de la respuesta
        if hasattr(response, 'content'):
            response_text = response.content
        elif isinstance(response, str):
            response_text = response
        else:
            response_text = str(response)
        
        # Intentar parsear como JSON
        try:
            # Buscar JSON en la respuesta
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(response_text)
        except json.JSONDecodeError:
            # Si no se puede parsear, retornar un análisis básico
            return {
                "match_score": 0.0,
                "status": "PENDIENTE",
                "skill_analysis": {
                    "hard_skills_score": 0.0,
                    "soft_skills_score": 0.0,
                    "matched_skills": [],
                    "missing_skills": []
                },
                "experience_score": 0.0,
                "compliance_check": {
                    "has_work_permit": candidato.has_work_permit,
                    "location_match": False,
                    "education_match": False
                },
                "recommendations": ["No se pudo procesar el análisis correctamente"],
                "summary": "Error al procesar la respuesta del agente",
                "detailed_analysis": response_text
            }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Obtiene información sobre el agente ATS
        
        Returns:
            Diccionario con información del agente
        """
        return {
            "system_name": "Simulador ATS con Análisis Semántico",
            "version": "2.0",
            "capabilities": [
                "Análisis semántico de habilidades",
                "Compliance checking automático",
                "Scoring ponderado (Hard Skills 50%, Experiencia 30%, Soft Skills 20%)",
                "Anonimización de datos PII",
                "Recomendaciones personalizadas"
            ],
            "instructions": settings.ats_system_instructions,
            "tools": ["GroqTools"],
            "model": "groq"
        }
