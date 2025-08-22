from pydantic import BaseModel
from .model_info import ModelInfo


class ModelList(BaseModel):
    providers: dict[str, list[ModelInfo]]