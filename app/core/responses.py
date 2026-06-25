from typing import Any


def success_response(message: str, data: Any = None, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta or {},
    }


def error_response(message: str, code: str, details: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "success": False,
        "message": message,
        "error": {
            "code": code,
            "details": details or [],
        },
    }
