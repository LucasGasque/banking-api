import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.serializers.root import AppInfo
from app.views import main_router
from app.configs.settings import settings
from app import __version__, app_info
from app.helpers.dump_sql import DumpSQL
from starlette_prometheus import PrometheusMiddleware, metrics


def add_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(PrometheusMiddleware)


def root() -> AppInfo:
    return app_info


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DumpSQL.dump_info()

    yield


def create_app() -> FastAPI:
    app = FastAPI(
        version=__version__,
        title=settings.APP_NAME,
        lifespan=lifespan,
    )
    add_middlewares(app)
    app.add_api_route("/", root, tags=["Info"], include_in_schema=False)  # type: ignore
    app.add_api_route("/metrics", metrics, tags=["Metrics"], include_in_schema=False)  # type: ignore
    app.include_router(main_router)

    return app


if __name__ == "__main__":
    uvicorn.run(create_app, host="0.0.0.0", port=8000)
