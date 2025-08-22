from pydantic import BaseModel, StringConstraints
from typing import Annotated


class LocationReference(BaseModel):
    location: Annotated[str, StringConstraints(min_length=3)]