from functools import cache
from typing import Awaitable, Callable, Union

from fastapi import Depends

from insight_extractor_ai_agent.logic.extract_insight import extract_insight
from insight_extractor_ai_agent.schemas.analysis_report import AnalysisReport

from ....services.analysis_service import AnalysisService
from ....utils.file_parser import FileParser


# Define the Extract Insight function as a dependency function
def get_extract_insight() -> Callable[[str, str, str, str, str], Awaitable[AnalysisReport]]:
    return extract_insight

# Instantiate the File Parser and return the get_content_from_file as a dependency function
@cache
def get_retrieve_content_from_file() -> Callable[[Union[str, bytes], str], tuple[str, str]]:
    return FileParser().get_content_from_file


# Instantiate the Analysis Service and return the get_analysis_service as a dependency function
@cache
def get_analysis_service(
    extract_insight: Callable[[str, str, str, str, str], Awaitable[AnalysisReport]] = Depends(get_extract_insight),
    retrieve_content_from_file: Callable[[Union[str, bytes], str], tuple[str, str]] = Depends(get_retrieve_content_from_file),
) -> AnalysisService:
    return AnalysisService(extract_insight=extract_insight, retrieve_content_from_file=retrieve_content_from_file)