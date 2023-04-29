import logging.config

from fastapi import FastAPI

import coloredlogs

from app.core.config import config, LOG_CONFIG
from app.routers.event import router as event_router


coloredlogs.install()
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

logger.info(f'Swagger url: {config.SERVER_HOST}/docs/')
logger.info(f'Redoc url: {config.SERVER_HOST}/redoc/')


app = FastAPI(
    title=config.PROJECT_NAME,
)


@app.get('/ping')
async def healtcheck():
    return 'pong'


app.include_router(event_router)
