import uvicorn
from config import config
from custom_logger import setup_logging
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from schemas.version import VersionSchema
from starlette_prometheus import PrometheusMiddleware, metrics

app = FastAPI(
    title="Name of service",
    version="0.00.15",
    description="OpenAPI schema",
    debug=config.DEBUG,
    dependencies=[],
    docs_url=None if config.ENV == 'prod' else "/docs",
    redoc_url=None if config.ENV == 'prod' else "/redoc",
)

FastAPIInstrumentor.instrument_app(app)
app.add_middleware(PrometheusMiddleware)

app.add_route("/metrics/", metrics)


@app.get("/version", response_model=VersionSchema)
async def version():
    return {"version": config.CI_COMMIT_SHA, "env": config.ENV}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa S104
        port=config.PORT,
        debug=config.DEBUG,
        reload=config.DEBUG,
        log_config=setup_logging(config.ENV == 'prod'),
        use_colors=True,
        log_level=config.LOG_LEVEL.lower(),
    )
