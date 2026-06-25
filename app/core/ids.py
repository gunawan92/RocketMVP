from uuid import UUID

from app.core.exceptions import ValidationAppError


def normalize_uuid(value: str, field: str = "id") -> str:
    try:
        return str(UUID(str(value)))
    except (TypeError, ValueError):
        raise ValidationAppError(
            "Validation error",
            details=[
                {
                    "field": field,
                    "message": "Value must be a valid UUID",
                }
            ],
        )
