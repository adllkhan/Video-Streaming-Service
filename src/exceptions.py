from http import HTTPStatus

from fastapi import HTTPException, status
from sqlalchemy.orm import DeclarativeMeta


class HTTPBaseException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: dict | None = None,
        message: str | None = None,
    ) -> None:
        if not detail:
            detail = {}
        if not message:
            message = "An unknown error occurred"
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "detail": detail,
                "status_code": status_code,
                "code": HTTPStatus(status_code).phrase.upper(),
            },
        )


class HTTPAlreadyExists(HTTPBaseException):
    def __init__(self, model: DeclarativeMeta, request: dict | None = None) -> None:
        message = f"{model.__name__.capitalize()} already exists!"
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"request": request},
            message=message,
        )
class HTTPNotFound(HTTPBaseException):
    def __init__(self, model: DeclarativeMeta, search: dict | None = None) -> None:
        message = f"{model.__name__.capitalize()} not found!"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"search": search},
            message=message,
        )

class HTTPValidationError(HTTPBaseException):
    def __init__(self, errors: dict | None = None) -> None:
        message = f"validation failed!"
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": errors},
            message=message,
        )        

class HTTPBadRequest(HTTPBaseException):
    def __init__(self, errors: dict | None = None) -> None:
        message = f"bad request!"
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors},
            message=message,
        )        