from typing import Annotated

from pydantic import BaseModel, StringConstraints


class LocationReference(BaseModel):
    location: Annotated[str, StringConstraints(min_length=3)]