from typing import Callable

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

from ...core.config.settings import settings


def generate_custom_openapi_docs(app: FastAPI) -> Callable[[], dict]:

    """

    Creates a custom OpenAPI schema generator that adds route-specific or global
    information to each route's description and metadata.

    
    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.

    Returns
    -------
    custom_openapi : Callable
        A function that returns the OpenAPI schema with custom information added.

    """

    if not isinstance(app, FastAPI):
        raise TypeError(f"app must be a FastAPI instance. Received: {app} with type {type(app)}")


    def _custom_openapi() -> dict:

        """

        Custom OpenAPI schema. 

        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.

        """

        # FastAPI caches the schema after it's built once. 
        # This check ensures it returns the cached version on subsequent calls to avoid recomputation.
        if app.openapi_schema:
            return app.openapi_schema

        # Generates the OpenAPI schema using FastAPI’s helper.
        # Pulls app title, version, description, and registered routes.
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )


        # APIRoute ensures we're only processing HTTP endpoints (not static files, WebSockets, etc.).
        # Skips anything that’s not a route with a method/handler.
        for route in app.routes:
            if not isinstance(route, APIRoute):
                continue

            # Extract rate limit from endpoint
            endpoint = route.endpoint
            raw_limit = getattr(endpoint, "__rate_limit__", None)

            # Normalize limit string
            limit_parts = []

            if raw_limit:
                limit_parts.append(", ".join(l.strip() for l in raw_limit.split(";")))
            else:
                limit_parts.append(", ".join(settings.RATE_LIMITS))

            # Compose full description limit
            full_limit_description = " + ".join(limit_parts)

            # Compose only the non-shared (global) limits for x-ratelimit-limit extension
            # These are the limits that come from raw_limit or settings.RATE_LIMITS only
            non_shared_limit_parts = []

            if raw_limit:
                non_shared_limit_parts.append(", ".join(l.strip() for l in raw_limit.split(";")))
            else:
                non_shared_limit_parts.append(", ".join(settings.RATE_LIMITS))

            non_shared_limit = " + ".join(non_shared_limit_parts)

            # Retrieves the Swagger path definition for this route (/health, /users, etc.).
            # If not found (edge case), skip it.
            path_item = openapi_schema["paths"].get(route.path)
            if not path_item:
                continue

            # Operation refers to HTTP methods under a path (e.g., get, post, etc.).
            # Adds a custom OpenAPI extension field: x-rateLimit, which external tools can parse.
            for operation in path_item.values():
                operation["x-ratelimit-limit"] = non_shared_limit
                # Appends a human-readable Markdown-formatted note to the endpoint’s Swagger description.
                # Uses strip() to remove any unwanted leading/trailing whitespace.
                existing_description = operation.get("description", "")
                rate_info = f"\n\n**Rate limit:** `{full_limit_description}`"
                operation["description"] = (existing_description + rate_info).strip()

        # Cache and return the schema
        app.openapi_schema = openapi_schema
        return app.openapi_schema


    # Return the callable generator
    return _custom_openapi