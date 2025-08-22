from pydantic import BaseModel


class ModelInfo(BaseModel):
    value: str 
    name: str