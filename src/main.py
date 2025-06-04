from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from config import Config
from src.api.v1.auth import router

app = FastAPI(
    debug=Config().SERVER_DEBUG,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    title="Video-Streaming API",
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=Config().SERVER_CORS_ORIGINS,
    allow_credentials=Config().SERVER_CREDENTIALS,
    allow_methods=Config().SERVER_METHODS,
    allow_headers=Config().SERVER_HEADERS,
)

app.include_router(router=router)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


if __name__ == "__main__":
    from uvicorn import run

    run(
        app="main:app",
        host=Config().SERVER_HOST,
        port=Config().SERVER_PORT,
        reload=Config().SERVER_RELOAD,
        app_dir="src",
    )
