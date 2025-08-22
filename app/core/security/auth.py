from ..exceptions.custom_http_exception import CustomHTTPException


def extract_api_key(authorization: str) -> str:

    """

    Extracts an API key from a Bearer token in the Authorization header.


    Parameters
    ----------
    authorization : str
        The value of the `Authorization` header.

    Returns
    -------
    api_key : str
        The extracted API key.

    """

    if not authorization.startswith("Bearer "):
        raise CustomHTTPException(
            status_code=401,
            detail="Invalid authorization scheme. Use 'Bearer <API_KEY>'."
        )
    

    api_key = authorization.split(" ", 1)[1].strip()

    if not api_key:
        raise CustomHTTPException(status_code=401, detail="API key is missing.")
    

    return api_key