from ..utils.class_importing_helper import import_class
from pydantic_ai import Agent
from ..schemas.analysis_report import AnalysisReport
from ..prompts.system.insight_extractor_agent_system_prompt import INSIGHT_EXTRACTOR_SYSTEM_PROMPT


async def extract_insight(model_name: str, api_key: str, content: str, file_name: str, file_type: str) -> AnalysisReport:
    
    """

    Initializes a dynamic AI agent and runs a content analysis.

    This function infers the provider and model from the model_name string
    (e.g., "openai:gpt-4o"), sets up the LLM, executes the analysis,
    and returns a structured report.

    
    Parameters
    ----------
    model_name : str
        Name of the language model in "provider:model" format.

    api_key : str
        API key to authenticate with the LLM provider.

    content : str
        The textual content to analyze.

    file_name : str
        Name of the file being analyzed.

    file_type : str
        Type of the file.
            The options are: 
                Text
                    `.txt`
                Markdown
                    `.md`
                JSON
                    `.json`
                CSV
                    `.csv`
                Python Code
                    `.py`
                JavaScript Code
                    `.js`
                PDF
                    `.pdf`
                Word Document
                    `.docx`
                Excel Spreadsheet
                    `.xlsx`
                HTML
                    `.html`
                XML
                    `.xml`

        
    Returns
    -------
    report : AnalysisReport
        The structured analysis report produced by the agent.

    """

    if not isinstance(model_name, str):
        raise TypeError(f"model_name must be a string. Received: {model_name} with type: {type(model_name)}")
    if not isinstance(api_key, str):
        raise TypeError(f"api_key must be a string. Received: {api_key} with type: {type(api_key)}")
    if not isinstance(content, str):
        raise TypeError(f"content must be a string. Received: {content} with type: {type(content)}")
    if not isinstance(file_name, str):
        raise TypeError(f"file_name must be a string. Received: {file_name} with type: {type(file_name)}")
    if not isinstance(file_type, str):
        raise TypeError(f"file_type must be a string. Received: {file_type} with type: {type(file_type)}")


    provider_key, model_key = model_name.split(":", 1)
    class_prefix = provider_key.capitalize()

    provider_class = import_class(
        f"pydantic_ai.providers.{provider_key}",
        f"{class_prefix}Provider"
    )
    model_class = import_class(
        f"pydantic_ai.models.{provider_key}",
        f"{class_prefix}Model"
    )


    model = model_class(
        model_name=model_key,
        provider=provider_class(api_key=api_key)
    )

    analysis_agent = Agent(
        model=model,
        output_type=AnalysisReport,
        system_prompt=INSIGHT_EXTRACTOR_SYSTEM_PROMPT,
        output_retries=3
    )


    response = await analysis_agent.run(content)
    report = response.output


    # Enrich the report with metadata
    report.file_name = file_name
    report.file_type_detected = file_type
    report.model_used = model_name


    return report