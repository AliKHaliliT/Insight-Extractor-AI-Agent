from typing import Any

from fastapi.exceptions import RequestValidationError


def generate_error_response_example(exc: BaseException) -> dict[str, Any]:

    """

    Generates a dictionary example from any exception instance.

    This utility dynamically extracts all public attributes of an exception 
    that do not begin with an underscore and are JSON-serializable, making 
    it suitable for use in API documentation as a structured example.

    
    Parameters
    ----------
    exc : BaseException
        Any exception instance to convert into an OpenAPI-compatible dictionary.

        
    Returns
    -------
    example : dict
        A dictionary containing serializable public attributes of the exception.

    """

    # Special case for FastAPI's RequestValidationError
    if exc == RequestValidationError:
        return {
            "title": "Validation Error",
            "detail": [
                {
                    "loc": ["body", "field_name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                    "input": "bad_value"
                }
            ],
            "status_code": 422,
            "type": "validation_error"
        }

    if not isinstance(exc, BaseException):
        raise TypeError(f"Expected an exception instance. Received: {exc} with type {type(exc)}")


    example = {}
    for attr in dir(exc):
        if attr.startswith("_"):
            continue  # Skip private and special attributes
        value = getattr(exc, attr)
        if callable(value):
            continue  # Skip methods
        if attr == "args":
            continue  # Skip
        try:
            # Check for JSON-serializable attribute
            import json
            json.dumps(value)
            example[attr] = value
        except (TypeError, ValueError):
            continue  # Skip unserializable fields


    return example
