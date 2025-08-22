from fastapi import Header
from ....core.security.auth import extract_api_key


# Get the API Key needed for analysis
def get_api_key(authorization: str = Header(...)) -> str:
    return extract_api_key(authorization)