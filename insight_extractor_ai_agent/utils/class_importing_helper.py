import importlib
from typing import Optional, Type


def import_class(module_path: str, class_name: str) -> Optional[Type]:

    """

    Dynamically import a class from a given module path.

    
    Parameters
    ----------
    module_path : str
        Full dotted path to the module (e.g., "pydantic_ai.providers.openai").
    class_name : str
        The class name to retrieve from the module.

        
    Returns
    -------
    cls : Type or None
        The imported class if found, otherwise None.

    """

    if not isinstance(module_path, str):
        raise TypeError(f"module_path must be a string. Received: {module_path} with type: {type(module_path)}")
    if not isinstance(class_name, str):
        raise TypeError(f"class_name must be a string. Received: {class_name} with type: {type(class_name)}")


    cls = getattr(importlib.import_module(module_path), class_name, None)

    if cls:
        print(f"Successfully imported class: {cls}")
    else:
        print(f"Error: Class `{class_name}` not found in `{module_path}`.")

    
    return cls