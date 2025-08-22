from typing import Callable, Awaitable, Union
from insight_extractor_ai_agent.schemas.analysis_report import AnalysisReport
from insight_extractor_ai_agent.logic.extract_insight import extract_insight
from functools import cache
from ....utils.file_parser import FileParser
from ....services.analysis_service import AnalysisService


# Define the Extract Insight function as a dependency function
def get_extract_insight() -> Callable[[str, str, str, str, str], Awaitable[AnalysisReport]]:
    return extract_insight

# Instantiate the File Parser and return the get_content_from_file as a dependency function
@cache
def get_content_from_file() -> Callable[[Union[str, bytes], str], tuple[str, str]]:
    return FileParser().get_content_from_file

@cache
def get_analysis_service() -> AnalysisService:
    return AnalysisService(extract_insight=get_extract_insight(), get_content_from_file=get_content_from_file())