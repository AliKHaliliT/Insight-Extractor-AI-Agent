from typing import Any

from pydantic import BaseModel


def generate_docs_response_example(model: type[BaseModel]) -> dict[str, Any]:

    """

    Generates a Swagger-style example dictionary from a Pydantic model.
    
    This function analyzes the JSON schema of a Pydantic model and produces an
    example dictionary that conforms to the model's structure and types. It 
    supports nested models and arrays with references.

    
    Parameters:
    -----------
    model : type[BaseModel]
        The Pydantic model class to generate the example from.

        
    Returns:
    --------
    example : dict
        A dictionary containing example values matching the model's schema.

    """

    if not isinstance(model, type) or not issubclass(model, BaseModel):
        raise TypeError(f"Input must be a Pydantic model class (subclass of BaseModel). Received: {model} with type {type(model)}")


    def _example_from_schema(props: dict[str, Any], defs: dict[str, Any]) -> dict[str, Any]:

        """

        Recursively generates example values for a given set of schema properties.

        
        Parameters:
        -----------
        props : dict
            The 'properties' section of a JSON schema.

        defs : dict
            A dictionary of referenced schema definitions.

            
        Returns:
        --------
        values_dictionary : dict
            Example values for the properties.

        """

        if not isinstance(props, dict):
            raise TypeError(f"props must be a dictionary. Received: {props} with type {type(props)}")
        if not isinstance(defs, dict):
            raise TypeError(f"defs must be a dictionary. Received: {defs} with type {type(defs)}")


        result = {}
        for key, val in props.items():
            if "$ref" in val:
                ref_key = val["$ref"].split("/")[-1]
                ref_schema = defs[ref_key]
                result[key] = _example_from_schema(ref_schema.get("properties", {}), defs)
            else:
                result[key] = _placeholder_from_type(val, defs)


        return result
    

    def _placeholder_from_type(field: dict[str, Any], defs: dict[str, Any]) -> Any:

        """

        Generates a placeholder example value for a field based on its type.

        
        Parameters:
        -----------
        field : dict
            The field schema.

        defs : dict
            A dictionary of referenced schema definitions.

            
        Returns:
        --------
        value : Any
            An example value for the field type.

        """

        if not isinstance(field, dict):
            raise TypeError(f"field must be a dictionary. Received: {field} with type {type(field)}")
        if not isinstance(defs, dict):
            raise TypeError(f"defs must be a dictionary. Received: {defs} with type {type(defs)}")

        
        t = field.get("type")
        if t == "string":
            return "string"
        if t == "integer":
            return 1
        if t == "number":
            return 1.0
        if t == "boolean":
            return True
        if t == "array":
            item = field.get("items", {})
            if "$ref" in item:
                ref_key = item["$ref"].split("/")[-1]
                item_schema = defs[ref_key]
                return [_example_from_schema(item_schema.get("properties", {}), defs)]
            else:
                return [_placeholder_from_type(item, defs)]
        if t == "object":
            return _example_from_schema(field.get("properties", {}), defs)
        return None
    

    schema = model.model_json_schema()


    return _example_from_schema(schema.get("properties", {}), schema.get("$defs", {}))