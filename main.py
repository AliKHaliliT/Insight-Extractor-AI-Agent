from app.core.config.setup import setup
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logging.logging_config import setup_logging
from app.core.config.settings import settings
from app.core.exception_handlers import (
    validation_exception_handler, 
    http_exception_handler, 
    general_exception_handler
)
from fastapi.exceptions import RequestValidationError, HTTPException
from slowapi.errors import RateLimitExceeded
from app.core.exception_handlers import rate_limit_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIASGIMiddleware
from app.core.middlewares import (
    AccessLogMiddleware, 
    RequestIDMiddleware, 
    StrictTransportSecurityMiddleware,
    XContentTypeOptionsMiddleware, 
    ContentSecurityPolicyMiddleware,
    PermissionsPolicyMiddleware,
    CrossOriginOpenerPolicyMiddleware,
    CrossOriginResourcePolicyMiddleware,
    CrossOriginEmbedderPolicyMiddleware,
    ReferrerPolicyMiddleware,
    XDownloadOptionsMiddleware,
    XFrameOptionsMiddleware,
    XXSSProtectionMiddleware,
    OriginAgentClusterMiddleware,
    NoCacheMiddleware,
    XDNSPrefetchControlMiddleware
)
from app.docs.logic.custom_openapi_docs import generate_custom_openapi_docs
from app.api.v1.routers.v1_router import v1_router
from fastapi import Request
from fastapi.responses import JSONResponse
import os
from fastapi.staticfiles import StaticFiles


# Startup Events
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Configure Logging
    setup_logging(handler_log_level=settings.HANDLER_LOG_LEVEL, 
                  root_log_level=settings.ROOT_LOG_LEVEL, 
                  uvicorn_log_level=settings.UVICORN_LOG_LEVEL)


    # SlowApi Setup
    app.state.limiter = setup.limiter


    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url=f"{settings.API_V1_PREFIX}{settings.DOCS_URL}",
    redoc_url=f"{settings.API_V1_PREFIX}{settings.REDOC_URL}",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)


# Configure Exception Handlers
## Custom Rate Limit Handler
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

## Custom Default Handlers 
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# Configure Middlewares
## Custom Access Logging
### Must come before the Request ID Middleware
app.add_middleware(AccessLogMiddleware)

## Request ID
app.add_middleware(RequestIDMiddleware)

## CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS
)

## Rate Limit
app.add_middleware(SlowAPIASGIMiddleware)

## Other Security Middlewares
app.add_middleware(StrictTransportSecurityMiddleware)
app.add_middleware(XContentTypeOptionsMiddleware)
### For demonstration purposes, security settings have been relaxed to make publishing and viewing the auto-generated documentation easier.
### In a real enterprise project, you should enforce stricter policies—avoid practices like "unsafe-inline" and instead use safer alternatives such as nonce.
### Additionally, the frontend here uses a development build of Tailwind. 
### In an enterprise environment, this should be properly optimized and prepared for production.
app.add_middleware(
    ContentSecurityPolicyMiddleware,
    policy=(
        "default-src 'self'; "
        
        # Scripts
        "script-src 'self'; "
        "script-src-elem 'self' "
        "https://cdn.tailwindcss.com "
        "https://cdn.jsdelivr.net "
        "https://cdnjs.cloudflare.com "
        "https://unpkg.com "
        "'unsafe-inline'; "
        
        # Workers
        "worker-src 'self' blob: https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        
        # Styles
        "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
        "style-src-elem 'self' https://fonts.googleapis.com https://cdn.jsdelivr.net 'unsafe-inline'; "
        
        # Fonts
        "font-src https://fonts.gstatic.com; "
        
        # Images
        "img-src 'self' data: "
        "https://fastapi.tiangolo.com "
        "https://cdn.redoc.ly "
        "https://cdn.jsdelivr.net; "
        
        # Misc
        "object-src 'none'; "
        "frame-ancestors 'none';"
    )
)
app.add_middleware(PermissionsPolicyMiddleware)
# app.add_middleware(CrossOriginOpenerPolicyMiddleware)
# app.add_middleware(CrossOriginEmbedderPolicyMiddleware)
app.add_middleware(CrossOriginResourcePolicyMiddleware)
app.add_middleware(ReferrerPolicyMiddleware)
app.add_middleware(XFrameOptionsMiddleware)
app.add_middleware(XXSSProtectionMiddleware, policy="1; mode=block")
app.add_middleware(XDownloadOptionsMiddleware)
app.add_middleware(OriginAgentClusterMiddleware)
app.add_middleware(NoCacheMiddleware)
app.add_middleware(XDNSPrefetchControlMiddleware)


# Configure docs
app.openapi = generate_custom_openapi_docs(app)


# APIs
## v1
app.include_router(v1_router, prefix=settings.API_V1_PREFIX)


static_dir = os.path.join(os.path.dirname(__file__), "app/static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates_dir = os.path.join(os.path.dirname(__file__), "app/templates")
app.mount("/", StaticFiles(directory=templates_dir, html=True), name="templates")


## Health Check
@app.get("/health")
async def health(request: Request):
    return JSONResponse(status_code=200, content={"message": "Insight Extractor AI Agent is UP and RUNNING!"})