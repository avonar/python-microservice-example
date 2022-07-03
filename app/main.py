from config import config
from fastapi import FastAPI

from schemas.version import VersionSchema
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from starlette_prometheus import PrometheusMiddleware, metrics

app = FastAPI(title="Name of service",
              version="0.00.15",
              description="OpenAPI schema",
              debug=config.DEBUG,
              dependencies=[],
              docs_url=None if config.ENV == 'prod' else "/docs",
              redoc_url=None if config.ENV == 'prod' else "/redoc")

FastAPIInstrumentor.instrument_app(app)
app.add_middleware(PrometheusMiddleware)


@app.get("/version", response_model=VersionSchema)
async def version():
    return {"version": config.CI_COMMIT_SHA, "env": config.ENV}


if __name__ == "__main__":
    uvicorn.run(
        "start:app",
        host="0.0.0.0",  # noqa S104
        port=config.PORT,
        debug=config.DEBUG,
        reload=config.DEBUG,
        log_config=logging_config,
        use_colors=True,
        log_level=config.LOG_LEVEL.lower(),
    )