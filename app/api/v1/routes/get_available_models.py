from typing import Callable

from fastapi import Depends, Request

from ....schemas.model_list import ModelList
from ..dependencies.get_available_models_factory import get_fetch_model_list


async def get_available_models(
    request: Request, 
    get_model_list: Callable[[], dict[str, list[dict[str, str]]]] = Depends(get_fetch_model_list)
) -> ModelList:

    """

    Endpoint to fetch the list of available models, grouped by provider.


    Parameters
    ----------
    None.

        
    Returns
    -------
    response : ModelList
        A JSON response containing the list of available models.
        
    """

    return ModelList(providers=get_model_list())