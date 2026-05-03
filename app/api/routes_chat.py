from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """
    Отправляет запрос к LLM и возвращает ответ
    """
    try:
        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=req.prompt,
            system=req.system,
            max_history=req.max_history,
            temperature=req.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/history")
async def get_history(
    limit: int = 10,
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """
    Возвращает последние сообщения пользователя
    """
    messages = await chat_usecase.get_history(user_id, limit)
    return {"messages": messages}


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """
    Удаляет историю сообщений пользователя
    """
    await chat_usecase.clear_history(user_id)
