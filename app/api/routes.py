from fastapi import APIRouter, HTTPException, status
from app.models.schemas import ATSMatchRequest, ATSMatchResponse, HealthResponse, SkillAnalysis, MatchStatus
from app.services import AgentService
from app.config import settings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter()

# Instancia del servicio del agente (singleton)
agent_service = None


def get_agent_service() -> AgentService:
    """Obtiene o crea la instancia del servicio del agente"""
    global agent_service
    if agent_service is None:
        try:
            agent_service = AgentService()
            logger.info("AgentService (Simulador ATS) inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar AgentService: {str(e)}")
            raise
    return agent_service


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - verifica que el servicio esté funcionando
    """
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version
    )


@router.get("/ats/info")
async def get_ats_info():
    """
    Obtiene información sobre el sistema ATS configurado
    """
    try:
        service = get_agent_service()
        return service.get_agent_info()
    except Exception as e:
        logger.error(f"Error al obtener información del ATS: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener información del ATS: {str(e)}"
        )


@router.post("/ats/match", response_model=ATSMatchResponse)
async def ats_matching(request: ATSMatchRequest):
    """
    Realiza el matching ATS entre una vacante y un candidato
    
    Este endpoint simula un Sistema de Seguimiento de Candidatos (ATS) con:
    - Análisis semántico de habilidades (no keyword matching exacto)
    - Compliance checking automático
    - Scoring ponderado: 50% Hard Skills, 30% Experiencia, 20% Soft Skills
    - Anonimización de datos PII para cumplir normativas de no discriminación
    
    Args:
        request: Objeto ATSMatchRequest con datos de vacante y candidato
        
    Returns:
        ATSMatchResponse con análisis completo del matching
    """
    try:
        logger.info(f"Procesando matching ATS para: {request.vacante.job_title}")
        
        # Obtener el servicio del agente
        service = get_agent_service()
        
        # Procesar el matching ATS
        analysis_result = service.process_ats_matching(
            vacante=request.vacante,
            candidato=request.candidato
        )
        
        logger.info(f"Matching completado - Score: {analysis_result.get('match_score', 0)}%")
        
        # Construir la respuesta estructurada
        response = ATSMatchResponse(
            match_score=analysis_result.get("match_score", 0.0),
            status=MatchStatus(analysis_result.get("status", "PENDIENTE")),
            skill_analysis=SkillAnalysis(
                hard_skills_score=analysis_result["skill_analysis"]["hard_skills_score"],
                soft_skills_score=analysis_result["skill_analysis"]["soft_skills_score"],
                matched_skills=analysis_result["skill_analysis"]["matched_skills"],
                missing_skills=analysis_result["skill_analysis"]["missing_skills"]
            ),
            experience_score=analysis_result.get("experience_score", 0.0),
            compliance_check=analysis_result.get("compliance_check", {}),
            recommendations=analysis_result.get("recommendations", []),
            summary=analysis_result.get("summary", ""),
            detailed_analysis=analysis_result.get("detailed_analysis", "")
        )
        
        return response
        
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de validación: {str(e)}"
        )
    except KeyError as e:
        logger.error(f"Error en formato de respuesta del agente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en el formato de respuesta del análisis: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error al procesar el matching ATS: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el matching ATS: {str(e)}"
        )
