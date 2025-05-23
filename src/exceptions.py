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
