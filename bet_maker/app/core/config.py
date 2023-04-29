from pydantic import BaseSettings


class Config(BaseSettings):
    API_STATUS: str

    SERVER_HOST: str

    PROJECT_NAME: str
    PROJECT_VERSION: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    RABBIT_SERVER: str
    RABBIT_USER: str
    RABBIT_PASSWORD: str
    RABBIT_EXCHANGE: str

    NEW_EVENT_QUEUE: str
    UPDATE_EVENT_QUEUE: str
    REMOVE_EVENT_QUEUE: str

    @property
    def RABBIT_URL(self) -> str:
        return (
            f'amqp://{self.RABBIT_USER}:'
            f'{self.RABBIT_PASSWORD}@'
            f'{self.RABBIT_SERVER}/%2F'
        )

    @property
    def POSTGRES_URL(self) -> str:
        return (
            f'postgresql://{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_SERVER}/'
            f'{self.POSTGRES_DB}'
        )

    @property
    def ASYNC_POSTGRES_URL(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_SERVER}/'
            f'{self.POSTGRES_DB}'
        )


    class Config:
        case_sensitive = True
        env_file = '.env'


config = Config()

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': 'coloredlogs.ColoredFormatter',
            'format': '%(asctime)s (%(levelname)s) %(name)s %(message)s'
        },
        'default': {'format': '%(asctime)s [%(process)s] %(levelname)s: %(message)s'}
    },
    'handlers': {
        'console': {
            'formatter': 'colored',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        }
    },
    'root': {'handlers': ['console']},
    'loggers': {
        'gunicorn': {'propagate': True},
        'gunicorn.access': {'propagate': True},
        'gunicorn.error': {'propagate': True},
        'uvicorn': {'propagate': True},
        'uvicorn.access': {'propagate': True},
        'uvicorn.error': {'propagate': True},
    }
}
