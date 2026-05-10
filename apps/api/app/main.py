from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import conversations, diagrams, health, prompts, codebase
from app.core.config import settings
from app.core.errors import AppError


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="AI Design System Diagram Assistant API",
    description="Backend API for design system diagram generation with AI enhancement.",
    version="0.1.0",
    lifespan=lifespan,
)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    status_code = 400
    if exc.code == "AI_TIMEOUT":
        status_code = 504 # Gateway Timeout or 408 Request Timeout
    
    return JSONResponse(
        status_code=status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "suggestion": exc.suggestion
        }
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "code": "NOT_FOUND",
            "message": f"Endpoint {request.method} {request.url.path} not found.",
            "suggestion": "Check the URL and try again."
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(prompts.router, prefix="/api/prompts", tags=["prompts"])
app.include_router(diagrams.router, prefix="/api/diagrams", tags=["diagrams"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])
app.include_router(codebase.router) # Prefix is already in the router
