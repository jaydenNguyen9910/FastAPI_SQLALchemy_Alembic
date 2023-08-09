import logging
import uuid
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.constant.master import ProjectBuildType, SwaggerPathURL
from app.core.exceptions import validation_exception_handler
from app.core.settings import settings
from app.routers import router

# Define app
app = FastAPI(title=settings.PROJECT_NAME,
              description=settings.PROJECT_DESCRIPTION,
              openapi_tags=settings.PROJECT_TAGS_METADATA,
              debug=settings.DEBUG, version=settings.VERSION,
              docs_url=None if settings.PROJECT_BUILD_TYPE == ProjectBuildType.PRODUCTION else SwaggerPathURL.DOCS,
              redoc_url=None if settings.PROJECT_BUILD_TYPE == ProjectBuildType.PRODUCTION else SwaggerPathURL.RE_DOC)

# Routers
app.include_router(router, prefix=settings.API_PREFIX)

# Logging config
@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{asctime} {levelprefix} : {message}",
        style="{", use_colors=True)
    logger.handlers[0].setFormatter(console_formatter)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
LOGGING_CONFIG = Path(__file__).parent / 'core/logging.conf'
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
logging.getLogger().level = logging.DEBUG if settings.DEBUG else logging.INFO

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
