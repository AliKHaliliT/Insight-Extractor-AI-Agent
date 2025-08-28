import os
import re

from slowapi import Limiter
from slowapi.util import get_remote_address

from ..config.settings import settings


def get_limiter(default_limits: list[str] = ["50/minute", "300/hour", "1000/day"]) -> Limiter:

    """

    Creates and returns a Limiter instance used for rate limiting in the application.
    
    Depending on the environment configuration, this function initializes the limiter with
    an in-memory backend or Redis backend.

    
    Parameters
    ----------
    default_limits : list, optional
        The default value(s) for the rate limit. The default value is `["50/minute", "300/hour", "1000/day"]`.
        If multiple rate limits are specified, all of those limits must be met. 

    
    Returns
    -------
    Limiter
        A configured instance of slowapi.Limiter with the appropriate backend.

    """

    if not isinstance(default_limits, list) or not all(isinstance(limit, str) and re.fullmatch(r"\d+/(minute|hour|day)", limit) for limit in default_limits):
        raise TypeError(f"default_limits must be a list of strings in the format '5/minute'. Received: {default_limits} with type {type(default_limits)}")


    # For headers_enabled to work, the reponse of the endpoint must be and insatnce of the starlette.responses.Response. 
    # JSONResponse from the FastAPI also works as it is using this in its definition. 
    # If the returned response is not an instance of Response and will be built at an upper level in the middleware stack, 
    # you'll need to provide the response object explicitly if you want the Limiter to modify the headers (headers_enabled=True):
    # @limiter.limit("5/minute")
    # async def myendpoint(request: Request, response: Response)
    # return {"key": "value"}
    if os.getenv("USE_REDIS"):
        return Limiter(
            key_func=get_remote_address,
            storage_uri=settings.REDIS_URL,
            default_limits=default_limits,
            headers_enabled=True,
        )
    return Limiter(key_func=get_remote_address, default_limits=default_limits, headers_enabled=True)