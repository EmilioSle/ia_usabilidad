from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum


class MatchStatus(str, Enum):
    """Estados posibles del matching"""
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
    PENDIENTE = "PENDIENTE"


class VacanteData(BaseModel):
    """Modelo para los datos de la vacante"""
    
    job_title: str = Field(..., description="Título del puesto")
    job_description: str = Field(..., description="Descripción completa del puesto")
    hard_skills: List[str] = Field(..., description="Habilidades técnicas requeridas")
    soft_skills: Optional[List[str]] = Field(None, description="Habilidades blandas deseadas")
    years_experience: int = Field(..., description="Años de experiencia requeridos")
    education: Optional[str] = Field(None, description="Nivel educativo requerido")
    languages: Optional[List[str]] = Field(None, description="Idiomas requeridos")
    location_required: Optional[str] = Field(None, description="Ubicación requerida")
    work_permit_required: bool = Field(default=True, description="¿Requiere permiso de trabajo?")
    sector: Optional[str] = Field(None, description="Sector o industria")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_title": "Desarrollador Frontend Senior",
                "job_description": "Buscamos un desarrollador con experiencia en React y TypeScript...",
                "hard_skills": ["React", "TypeScript", "CSS", "Git"],
                "soft_skills": ["Trabajo en equipo", "Comunicación efectiva"],
                "years_experience": 3,
                "education": "Ingeniería en Sistemas o afín",
                "languages": ["Español", "Inglés intermedio"],
                "location_required": "Ciudad de México",
                "work_permit_required": True,
                "sector": "Tecnología"
            }
        }


class CandidatoData(BaseModel):
    """Modelo para los datos del candidato"""
    
    cv_text: str = Field(..., description="Texto completo del CV")
    skills: List[str] = Field(..., description="Habilidades y tecnologías")
    years_experience: int = Field(..., description="Años de experiencia total")
    education: str = Field(..., description="Nivel educativo alcanzado")
    languages: List[str] = Field(..., description="Idiomas que habla")
    location: str = Field(..., description="Ubicación actual")
    has_work_permit: bool = Field(..., description="¿Tiene permiso de trabajo?")
    sector_experience: Optional[str] = Field(None, description="Experiencia en sector específico")
    additional_info: Optional[str] = Field(None, description="Información adicional relevante")
    
    class Config:
        json_schema_extra = {
            "example": {
                "cv_text": "Desarrollador Frontend con 4 años de experiencia trabajando con React, TypeScript y Next.js...",
                "skills": ["React", "TypeScript", "Next.js", "CSS", "Git", "Jest"],
                "years_experience": 4,
                "education": "Ingeniería en Sistemas Computacionales",
                "languages": ["Español nativo", "Inglés avanzado"],
                "location": "Ciudad de México",
                "has_work_permit": True,
                "sector_experience": "Tecnología y Startups",
                "additional_info": "Experiencia liderando equipos pequeños"
            }
        }


class ATSMatchRequest(BaseModel):
    """Modelo para la petición del matching ATS"""
    
    vacante: VacanteData = Field(..., description="Datos de la vacante")
    candidato: CandidatoData = Field(..., description="Datos del candidato")
    
    class Config:
        json_schema_extra = {
            "example": {
                "vacante": {
                    "job_title": "Desarrollador Frontend Senior",
                    "job_description": "Buscamos desarrollador con experiencia en React",
                    "hard_skills": ["React", "TypeScript", "CSS"],
                    "soft_skills": ["Trabajo en equipo"],
                    "years_experience": 3,
                    "education": "Ingeniería",
                    "languages": ["Español", "Inglés"],
                    "location_required": "Ciudad de México",
                    "work_permit_required": True,
                    "sector": "Tecnología"
                },
                "candidato": {
                    "cv_text": "Desarrollador con 4 años de experiencia en React...",
                    "skills": ["React", "TypeScript", "Next.js"],
                    "years_experience": 4,
                    "education": "Ingeniería en Sistemas",
                    "languages": ["Español", "Inglés"],
                    "location": "Ciudad de México",
                    "has_work_permit": True,
                    "sector_experience": "Tecnología"
                }
            }
        }


class SkillAnalysis(BaseModel):
    """Análisis de habilidades"""
    hard_skills_score: float = Field(..., description="Score de habilidades técnicas (0-100)")
    soft_skills_score: float = Field(..., description="Score de habilidades blandas (0-100)")
    matched_skills: List[str] = Field(..., description="Habilidades que coinciden")
    missing_skills: List[str] = Field(..., description="Habilidades faltantes")


class ATSMatchResponse(BaseModel):
    """Modelo para la respuesta del matching ATS"""
    
    match_score: float = Field(..., description="Score de afinidad (0-100)", ge=0, le=100)
    status: MatchStatus = Field(..., description="Estado del matching")
    skill_analysis: SkillAnalysis = Field(..., description="Análisis detallado de habilidades")
    experience_score: float = Field(..., description="Score de experiencia (0-100)", ge=0, le=100)
    compliance_check: Dict[str, bool] = Field(..., description="Verificación de requisitos legales")
    recommendations: List[str] = Field(..., description="Recomendaciones para el candidato")
    summary: str = Field(..., description="Resumen ejecutivo del análisis")
    detailed_analysis: str = Field(..., description="Análisis detallado completo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "match_score": 85.5,
                "status": "APROBADO",
                "skill_analysis": {
                    "hard_skills_score": 90.0,
                    "soft_skills_score": 80.0,
                    "matched_skills": ["React", "TypeScript", "CSS"],
                    "missing_skills": ["Docker"]
                },
                "experience_score": 85.0,
                "compliance_check": {
                    "has_work_permit": True,
                    "location_match": True,
                    "education_match": True
                },
                "recommendations": [
                    "Considerar aprendizaje de Docker",
                    "Certificación en React avanzado"
                ],
                "summary": "Candidato altamente calificado con excelente match técnico",
                "detailed_analysis": "El candidato presenta un perfil sólido..."
            }
        }


class HealthResponse(BaseModel):
    """Modelo para el endpoint de health check"""
    
    status: str = Field(..., description="Estado del servicio")
    app_name: str = Field(..., description="Nombre de la aplicación")
    version: str = Field(..., description="Versión de la aplicación")
