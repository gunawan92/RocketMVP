from collections.abc import Callable

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.responses import error_response


class AppError(Exception):
    def __init__(self, message: str, code: str = "INTERNAL_SERVER_ERROR", http_status_code: int = 500):
        self.message = message
        self.code = code
        self.http_status_code = http_status_code
        super().__init__(message)


class ValidationAppError(AppError):
    def __init__(self, message: str, details: list[dict] | None = None):
        self.details = details or []
        super().__init__(message, code="VALIDATION_ERROR", http_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class BusinessRuleError(AppError):
    def __init__(self, message: str, details: list[dict] | None = None):
        self.details = details or []
        super().__init__(message, code="BUSINESS_RULE_ERROR", http_status_code=status.HTTP_400_BAD_REQUEST)


class ResourceNotFoundError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, code="RESOURCE_NOT_FOUND", http_status_code=status.HTTP_404_NOT_FOUND)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        details = getattr(exc, "details", [])
        return JSONResponse(
            status_code=exc.http_status_code,
            content=error_response(message=exc.message, code=exc.code, details=details),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        details = []
        for item in exc.errors():
            location = item.get("loc", [])
            field = ".".join(str(part) for part in location if part != "body") or "body"
            details.append({"field": field, "message": item.get("msg", "Invalid input")})

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response(
                message="Validation error",
                code="VALIDATION_ERROR",
                details=details,
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response(
                message="Internal server error",
                code="INTERNAL_SERVER_ERROR",
                details=[],
            ),
        )
