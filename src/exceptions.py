from http import HTTPStatus

from fastapi import HTTPException, status
from sqlalchemy.orm import DeclarativeMeta


class HTTPBaseException(HTTPException):
    def __init__(
        self,
        status_code: int,
        details: dict | None = None,
        message: str | None = None,
    ) -> None:
        if not details:
            details = {}
        if not message:
            message = "An unknown error occurred"
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "details": details,
                "status_code": status_code,
                "code": HTTPStatus(status_code).phrase.upper(),
            },
        )


class HTTPAlreadyExists(HTTPBaseException):
    def __init__(self, model: DeclarativeMeta, request: dict | None = None) -> None:
        message = f"{model.__name__.capitalize()} already exists!"
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            details={"request": request},
            message=message,
        )


class HTTPNotFound(HTTPBaseException):
    def __init__(self, model: DeclarativeMeta, request: dict | None = None) -> None:
        message = f"{model.__name__.capitalize()} not found."
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            details={"request": request},
            message=message,
        )


class HTTPInvalidToken(HTTPBaseException):
    def __init__(self) -> None:
        message = "Invalid token provided."
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=None,
            message=message,
        )
