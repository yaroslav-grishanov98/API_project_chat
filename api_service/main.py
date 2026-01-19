from fastapi import FastAPI
from api_service.api.v1.endpoints import chats


def create_application() -> FastAPI:
    """Создает и конфигурирует экземпляр FastAPI приложения."""
    application = FastAPI(
        title="Chat API Service",
        description="API for managing chats and messages",
        version="1.0.0",
    )

    application.include_router(chats.router, prefix="/v1/chats", tags=["chats"])

    @application.get("/")
    async def read_root():
        return {"message": "Welcome to the Chat API Service!"}

    return application


app = create_application()
