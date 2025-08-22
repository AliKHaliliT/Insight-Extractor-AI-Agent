from fastapi import HTTPException
from typing import Union, Any, Optional


class CustomHTTPException(HTTPException):

    """

    Base exception for the Inference API.

    Usage:
    ------
    This supports inheritance or usage patterns like the following. 
    ```
    raise CustomHTTPException(
        status_code=500,
        detail="Internal server error",
        headers={"X-Error-Type": "inference_error"}
    )
    ```
    
    """

    def __init__(self,
                 status_code: int = 500,
                 detail: Union[str, dict[str, Any], list[Any]] = "An unexpected error occurred during inference.",
                 headers: Optional[dict[str, str]] = None,
                 title: Optional[str] = "Internal Server Error",
                 error_type: Optional[str] = None) -> None:
        
        """

        Constructor for the Custom HTTP Inference Exception.

        
        Parameters
        ----------
        status_code : int, optional
            HTTP status code for the exception. The default value is `500`.

        detail : str or dict or list, optional
            Detailed error message or object. The default value is `"Internal server error"`.

        headers : dict, optional
            Headers to include in the HTTP response. The default value is `None`.

        title : str, optional
            Title of the error. The default value is `None`. If `None`, defaults to `"Error"`.

        error_type : str, optional
            Type of the error, The default value is `None`. If `None`, defaults to `"inference_error"`.

            
        Returns
        -------
        None.

        """

        super().__init__(status_code=status_code, detail=detail, headers=headers)

        self.title = title or "Error"
        self.error_type = error_type or "inference_error"