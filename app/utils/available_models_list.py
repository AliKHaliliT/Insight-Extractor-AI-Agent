
from typing import Literal, get_args

from pydantic_ai.models import KnownModelName


def fetch_model_list() -> dict[str, list[dict[str, str]]]:

    """

    Parses the KnownModelName TypeAliasType literal from the pydantic-ai framework to create a structured 
    dictionary of providers and models, with special handling for 'google-gla' and 'google-vertex'. 
    The removal of this edge case is contingent on the removal of deprecated items in a future Pydantic-AI release.

    
    Parameters
    ----------
    None

    
    Returns
    -------
    structured_models : dict
        Dictionary of providers and their associated models. 
            Each entry contains:
                "value" : str  
                    Full provider:model string (e.g., "openai:gpt-4o").
                "name" : str  
                    Extracted model name (e.g., "gpt-4o").

    """

    inner_literal = next(
        v for k, v in vars(KnownModelName).items() 
        if isinstance(v, type(Literal['a']))
    )
    model_list = get_args(inner_literal)
    

    structured_models: dict[str, list[dict[str, str]]] = {}

    for model_string in sorted(model_list):
        try:
            provider, model_name = model_string.split(':', 1)

            # Check if the provider is a Google one and unify it
            if provider in ["google-gla", "google-vertex"]:
                provider = "google"

            # Simple title casing for provider display name
            provider_display = provider.replace('-', ' ').replace('_', ' ').title()
            
            if provider_display not in structured_models:
                structured_models[provider_display] = []

            # Check for uniqueness before appending the model
            is_unique = True
            for existing_model in structured_models[provider_display]:
                if existing_model["name"] == model_name:
                    is_unique = False
                    break
            
            if is_unique:
                structured_models[provider_display].append({
                    "value": f"{provider}:{model_name}",
                    "name": model_name
                })
        except ValueError:
            continue
            

    # Sort providers alphabetically
    return dict(sorted(structured_models.items()))