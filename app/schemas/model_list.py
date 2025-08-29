from pydantic import RootModel

from .model_info import ModelInfo


class ModelList(RootModel[dict[str, list[ModelInfo]]]):
    pass