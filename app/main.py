import logging

import uvicorn
from config import config
from custom_logger import setup_logging
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from schemas.user import UserCreate, UserRead, UserUpdate
from schemas.version import VersionSchema
from starlette_prometheus import PrometheusMiddleware, metrics
from users import auth_backend, fastapi_users, google_oauth_client

app = FastAPI(
    title="Name of service",
    version="0.00.15",
    description="OpenAPI schema",
    debug=config.DEBUG,
    dependencies=[],
    docs_url=None if config.ENV == 'prod' else "/docs",
    redoc_url=None if config.ENV == 'prod' else "/redoc",
    prefix="/api",
)

app.add_middleware(PrometheusMiddleware)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, "SECRET"),
    prefix="/auth/google",
    tags=["auth"],
)

FastAPIInstrumentor.instrument_app(app)
app.add_route("/metrics/", metrics)

setup_logging(config.ENV == 'prod')
logger = logging.getLogger(__name__)


@app.get("/version", response_model=VersionSchema)
async def version():
    logger.info("version")
    return {"version": config.CI_COMMIT_SHA, "env": config.ENV}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa S104
        port=config.PORT,
        debug=config.DEBUG,
        reload=config.DEBUG,
        use_colors=True,
        log_config=None,
        access_log=True,
    )
