from logging import getLogger
from fastapi import UploadFile
from typing import Callable, Awaitable, Union, Tuple
from insight_extractor_ai_agent.schemas.analysis_report import AnalysisReport


logger = getLogger(__name__)


class AnalysisService:

    """

    Service responsible for document analysis workflow, including API key extraction,
    file parsing, and AI insight extraction.

    
    Usage:
    ------
    ```python
    service = AnalysisService(extract_insight, get_content_from_file)
    report = await service.analyze_document(file, api_key, model_name)
    ```

    """

    def __init__(
        self,
        extract_insight: Callable[[str, str, str, str, str], Awaitable[AnalysisReport]],
        get_content_from_file: Callable[[Union[str, bytes], str], Tuple[str, str]],
    ) -> None:
        
        """

        Constructor for AnalysisService.

        
        Parameters
        ----------
        extract_insight : Callable
            Dependency that performs AI-based insight extraction.

        get_content_from_file : Callable
            Dependency that parses file bytes into content and file_type.


        Returns
        -------
        None.

        """
        
        self.extract_insight = extract_insight
        self.get_content_from_file = get_content_from_file


    async def analyze_document(self, file: UploadFile, api_key: str, model_name: str) -> AnalysisReport:

        """

        Main document analysis workflow.

        Steps
        -----
        1. Parse the uploaded file to retrieve content and type.
        2. Call the AI insight extraction dependency.

        
        Parameters
        ----------
        file : UploadFile
            The uploaded file to analyze.

        api_key : str
            The API key to use for analysis.

        model_name : str
            The AI model to use for analysis.


        Returns
        -------
        result : AnalysisReport
            The analysis report returned by the AI extraction dependency.


        """

        logger.info("Starting document analysis workflow.")

        # Step 1: Parse file using injected dependency
        file_content_bytes = await file.read()
        content, file_type = self.get_content_from_file(file_content_bytes, file.filename)
        logger.info(f"File {file.filename} parsed successfully.")

        # Step 2: Run AI insight extraction
        result = await self.extract_insight(
            api_key=api_key,
            model_name=model_name,
            content=content,
            file_name=file.filename,
            file_type=file_type,
        )
        logger.info("AI analysis completed successfully.")


        return result