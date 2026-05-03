import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    """
    Клиент для взаимодействия с OpenRouter API
    """
    def __init__(
        self,
        api_key: str = settings.OPENROUTER_API_KEY,
        base_url: str = settings.OPENROUTER_BASE_URL,
        site_url: str = settings.OPENROUTER_SITE_URL,
        app_name: str = settings.OPENROUTER_APP_NAME,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.site_url = site_url
        self.app_name = app_name
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """
        Создаёт клиент
        """
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.app_name,
                    "Content-Type": "application/json",
                }
            )
        return self._client

    async def close(self) -> None:
        """
        Закрывает клиент
        """
        if self._client:
            await self._client.aclose()
            self._client = None

    async def chat_completion(
        self,
        messages: list[dict],
        model: str = settings.OPENROUTER_MODEL,
        temperature: float = 0.7,
    ) -> str:
        """
        Отправляет запрос к OpenRouter и возвращает ответ
        """
        client = await self._get_client()
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }

        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            detail = f"OpenRouter returned {e.response.status_code}: {e.response.text}"
            raise ExternalServiceError(detail) from e
        except httpx.RequestError as e:
            detail = f"Failed to connect to OpenRouter: {str(e)}"
            raise ExternalServiceError(detail) from e

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            detail = f"Unexpected response format from OpenRouter: {data}"
            raise ExternalServiceError(detail) from e
