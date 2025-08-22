from typing import Callable
from ....utils.available_models_list import fetch_model_list


# Define the Fetch Model List function as a dependency function
def get_fetch_model_list() -> Callable[[], dict[str, list[dict[str, str]]]]:
    return fetch_model_list