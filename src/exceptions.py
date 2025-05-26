from fastapi import HTTPException, status


class HTTPBaseException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: dict | None = None,
        message: str | None = None,
        code: str | None = None,
    ) -> None:
        if not detail:
            detail = {}
        if not message:
            message = "An unknown error occurred"
        if not code:
            code = "UNKNOWN_ERROR"
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "detail": detail,
                "status_code": status_code,
                "code": code,
            },
        )


class HTTPAlreadyExists(HTTPBaseException):
    def __init__(self, model: str, request: dict | None = None) -> None:
        message = f"{model.capitalize()} already exists"
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"request": request},
            message=message,
            code="CONFLICT",
        )


class HTTPNotFound(HTTPBaseException):
    def __init__(self, model: str, search: dict | None = None) -> None:
        message = f"{model.capitalize()} not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"search": search},
            message=message,
            code="NOT_FOUND",
        )


class HTTPValidationError(HTTPBaseException):
    def __init__(self, errors: dict | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors,
            message="Validation failed",
            code="VALIDATION_ERROR",
        )


class HTTPDatabaseError(HTTPBaseException):
    def __init__(self, error: str) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"db_error": error},
            message="Database error occurred",
            code="DB_ERROR",
        )


class HTTPUnauthorized(HTTPBaseException):
    def __init__(self, reason: str = "Unauthorized") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"reason": reason},
            message="Unauthorized access",
            code="UNAUTHORIZED",
        )


class HTTPForbidden(HTTPBaseException):
    def __init__(self, reason: str = "Forbidden") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"reason": reason},
            message="Permission denied",
            code="FORBIDDEN",
        )
