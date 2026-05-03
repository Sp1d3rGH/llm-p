from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router
from app.services.openrouter_client import OpenRouterClient
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Создание таблиц БД и клиента OpenRouter при старте приложения
    """
    openrouter_client = OpenRouterClient()
    app.state.openrouter_client = openrouter_client

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await openrouter_client.close()
    await engine.dispose()


def create_app() -> FastAPI:
    """
    Создаёт и настраивает FastAPI
    """
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(chat_router, prefix="/chat", tags=["chat"])

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "environment": settings.ENV}

    return app


app = create_app()
