from fastapi import Depends, File, Form, Request, UploadFile

from insight_extractor_ai_agent.schemas.analysis_report import AnalysisReport

from ....services.analysis_service import AnalysisService
from ..dependencies.common import get_api_key
from ..dependencies.get_analyze_document_factory import get_analysis_service


async def analyze_document(
    request: Request,
    file: UploadFile = File(...),
    model_name: str = Form(...),
    api_key: str = Depends(get_api_key),
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisReport:
    
    """

    Endpoint to analyze an uploaded document.

    This endpoint is a thin wrapper around the AnalysisService, which performs
    the workflow of API key extraction, file parsing, and AI insight extraction.

    
    Parameters
    ----------
    request : Request
        The FastAPI request object.

    file : UploadFile
        The uploaded document.

    model_name : str
        The name of the AI model to use.

        
    Returns
    -------
    analysis_report : AnalysisReport
        The AI-generated analysis report.
        
    """

    return await service.analyze_document(file, api_key, model_name)