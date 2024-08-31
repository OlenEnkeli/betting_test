import logging.config

import coloredlogs
from fastapi import FastAPI

from app.core.config import LOG_CONFIG, config
from app.routers.bet import router as bet_router
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
app.include_router(bet_router)
