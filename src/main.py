from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router
from config import Config

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

if __name__ == "__main__":
    from uvicorn import run

    run(
        app="main:app",
        host=Config().SERVER_HOST,
        port=Config().SERVER_PORT,
        reload=Config().SERVER_RELOAD,
    )
