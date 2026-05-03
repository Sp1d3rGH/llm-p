class AppError(Exception):
    """
    Базовая ошибка приложения
    """
    def __init__(
        self,
        detail: str = "An application error occurred",
        status_code: int = 500
    ):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class ConflictError(AppError):
    """
    Конфликт данных
    """
    def __init__(self, detail: str = "Resource conflict"):
        super().__init__(detail=detail, status_code=409)


class UnauthorizedError(AppError):
    """
    Неверные учётные данные или отсутствие аутентификации
    """
    def __init__(self, detail: str = "Invalid authentication credentials"):
        super().__init__(detail=detail, status_code=401)


class ForbiddenError(AppError):
    """
    Доступ запрещён (недостаточно прав)
    """
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(detail=detail, status_code=403)


class NotFoundError(AppError):
    """
    Запрашиваемый объект не найден
    """
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail=detail, status_code=404)


class ExternalServiceError(AppError):
    """
    Ошибка при обращении к внешнему сервису OpenRouter
    """
    def __init__(self, detail: str = "External service error"):
        super().__init__(detail=detail, status_code=502)
