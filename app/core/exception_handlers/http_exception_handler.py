from logging import getLogger

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from ...docs.logic.error_response import create_error_response

logger = getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:

    """

    Handler for standard FastAPI HTTPExceptions not caught by custom exceptions.

    
    Parameters
    ----------
    request : Request
        The incoming request object.

    exc : HTTPException
        The HTTP Exception instance caught.

        
    Returns
    -------
    JSONResponse
        A JSON response detailing the HTTP error.

    """

    logger.error(f"HTTP Exception: {exc.status_code}: {exc.detail}")


    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            title=f"HTTP Error {exc.status_code}",
            detail=exc.detail,
            status_code=exc.status_code,
            error_type="http_error"
        ),
        headers=exc.headers
    )