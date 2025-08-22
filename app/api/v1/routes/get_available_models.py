from fastapi import Request, Depends
from typing import Callable
from ..dependencies.get_available_models_factory import get_fetch_model_list
from fastapi.responses import JSONResponse


async def get_available_models(
    request: Request, 
    get_model_list: Callable[[], dict[str, list[dict[str, str]]]] = Depends(get_fetch_model_list)
) -> JSONResponse:

    """

    Endpoint to fetch the list of available models, grouped by provider.


    Parameters
    ----------
    None.

        
    Returns
    -------
    response : JSONResponse
        A JSON response containing the list of available models.
        
    """

    return JSONResponse(content=get_model_list())