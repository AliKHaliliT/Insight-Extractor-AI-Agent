from logging import getLogger

from fastapi import Request, status
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from ...docs.logic.error_response import create_error_response

logger = getLogger(__name__)


async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    
    """

    Handler for SlowAPI's RateLimitExceeded exception that returns a custom-styled JSON error response
    and adds rate limit headers to the response.

    
    Parameters
    ----------
    request : Request
        The incoming request object.

    exc : RateLimitExceeded
        The SlowAPI exception instance indicating a rate limit breach.

        
    Returns
    -------
    JSONResponse
        A JSON response with a custom error format and appropriate rate limit headers.

    """

    logger.warning(f"Rate limit exceeded for request: {request.url}")
    
    
    # Create the base JSON response
    response = JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=create_error_response(
            title="Rate limit exceeded",
            detail="You have sent too many requests. Please try again later.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_type="rate_limit_exceeded"
        )
    )


    request.app.state.limiter._inject_headers(
        response,
        request.state.view_rate_limit
    )


    return response