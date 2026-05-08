from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import conversations, diagrams, health, prompts
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="AI Design System Diagram Assistant API",
    description="Backend API for design system diagram generation with AI enhancement.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(prompts.router, tags=["prompts"])
app.include_router(diagrams.router, tags=["diagrams"])
app.include_router(conversations.router, tags=["conversations"])
