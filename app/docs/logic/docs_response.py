from typing import Any


def create_docs_response(description: str, example: dict[str, Any]) -> dict[str, Any]:

    """
    
    Method to create a customized docs response.


    Parameters
    ----------
    description : str
        Message description.

    example : dict
        Example.
        
        
    Returns
    -------
    response : dict
        Customized response.
    
    """

    if not isinstance(description, str):
        raise TypeError(f"description must be a string. Received: {description} with type {type(description)}")
    if not isinstance(example, dict):
        raise TypeError(f"example must be a dict. Received: {example} with type {type(example)}")
    

    return {
        "description": description,
        "content": {
            "application/json": {
                "example": example
            }
        }
    }