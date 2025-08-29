from fastapi import APIRouter
from fastapi.exceptions import RequestValidationError

from insight_extractor_ai_agent.schemas.analysis_report import AnalysisReport

from ....core.exceptions.custom_http_exception import CustomHTTPException
from ....docs.logic.docs_response import create_docs_response
from ....docs.logic.docs_response_example import generate_docs_response_example
from ....docs.logic.error_response_example import \
    generate_error_response_example
from ....schemas.model_list import ModelList
from ..routes.analyze_document import analyze_document
from ..routes.get_available_models import get_available_models

v1_router = APIRouter(tags=["All Routes"])


v1_router.add_api_route(
    "/get-available-models",
    get_available_models,
    methods=["GET"],
    responses={
        200: create_docs_response("Successful Response", generate_docs_response_example(ModelList)),
        422: create_docs_response("Validation Error", generate_error_response_example(RequestValidationError)),
        500: create_docs_response("Internal Server Error", generate_error_response_example(CustomHTTPException()))
    }
)

v1_router.add_api_route(
    "/analyze-document",
    analyze_document,
    methods=["POST"],
    responses={
        200: create_docs_response("Successful Response", generate_docs_response_example(AnalysisReport)),
        422: create_docs_response("Validation Error", generate_error_response_example(RequestValidationError)),
        500: create_docs_response("Internal Server Error", generate_error_response_example(CustomHTTPException()))
    }
)