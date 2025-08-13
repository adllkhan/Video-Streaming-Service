from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from scalar_fastapi import Layout, Theme, get_scalar_api_reference
from starlette.exceptions import HTTPException

from core.config import config
from routers import router

app = FastAPI(
    debug=config.SERVER_DEBUG,
    openapi_url="/.well-known/openapi.json",
    docs_url="/api/swagger",
    redoc_url="/api/redoc",
    title="Video-Streaming API",
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=config.SERVER_CORS_ORIGINS,
    allow_credentials=config.SERVER_CREDENTIALS,
    allow_methods=config.SERVER_METHODS,
    allow_headers=config.SERVER_HEADERS,
)

app.include_router(router=router)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@app.get("/api/docs", include_in_schema=False)
async def scalar_html() -> HTMLResponse:
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        theme=Theme.BLUE_PLANET,
        scalar_theme=None,
        layout=Layout.CLASSIC,
        hide_models=True,
    )


if __name__ == "__main__":
    from uvicorn import run

    run(
        app="main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=config.SERVER_RELOAD,
    )
