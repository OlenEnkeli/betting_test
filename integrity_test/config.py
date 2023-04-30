from pydantic import BaseSettings


class Config(BaseSettings):

    LINE_PROVER_API_URL: str
    BET_MAKER_API_URL: str

    class Config:
        case_sensitive = True
        env_file = '.env'


config = Config()
