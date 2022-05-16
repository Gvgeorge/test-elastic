from pydantic import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):

    server_host: str = '0.0.0.0'
    server_port: int = 5555
    database_url: str = 'sqlite:///./database.sqlite3'
    elastic_host: str = '0.0.0.0'
    elastic_port: int = 9200
    elastic_index: str = 'search_service'


settings = Settings()
