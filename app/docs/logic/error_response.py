from typing import Any, Optional


def create_error_response(title: str, 
                          detail: Any, 
                          status_code: int, 
                          error_type: Optional[str] = None) -> dict[str, Any]:

    """
    
    Method to create a customized error response.


    Parameters
    ----------
    title : str
        Message title.

    detail : Any
        Message detail.

    status_code : int
        Status code.

    error_type : str, optional
        Error type. The default value is `None`.
        
        
    Returns
    -------
    response : dict
        Customized response.
    
    """

    if not isinstance(title, str):
        raise TypeError(f"title must be a string. Received: {title} with type {type(title)}")
    if not isinstance(detail, (str, dict, list)):
        raise TypeError(f"detail must be a string, dict, or list. Received: {detail} with type {type(detail)}")
    if not isinstance(status_code, int):
        raise TypeError(f"status_code must be an integer. Received: {status_code} with type {type(status_code)}")
    if error_type is not None and not isinstance(error_type, str):
        raise TypeError(f"error_type must be a string. Received: {error_type} with type {type(error_type)}")


    return {
        "title": title,
        "detail": detail,
        "status_code": status_code,
        "type": error_type or "error"
    }