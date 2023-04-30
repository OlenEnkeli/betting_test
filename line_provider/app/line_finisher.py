import asyncio
import logging

import coloredlogs

from app.core.config import LOG_CONFIG
from app.services.line_finisher import line_finisher


if __name__ == '__main__':
    coloredlogs.install()
    logging.config.dictConfig(LOG_CONFIG)
    asyncio.run(line_finisher())
