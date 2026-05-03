from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Запрос к чату с LLM
    """
    prompt: str = Field(...,
        min_length=1,
        description="Текст сообщения пользователя",
    )
    system: str | None = Field(
        None,
        description="Системная инструкция (необязательно)",
    )
    max_history: int = Field(
        12,
        ge=0,
        description="Максимальное количество последних сообщений из истории",
    )
    temperature: float = Field(
        0.7,
        ge=0.0,
        description="Температура, управление “креативностью” модели",
    )


class ChatResponse(BaseModel):
    """
    Ответ чата LLM
    """
    answer: str = Field(..., description="Ответ модели")
