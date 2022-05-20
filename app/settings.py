from pydantic import BaseSettings
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):

    server_host: str = '0.0.0.0'
    server_port: int = 5555
    database_url: str = f'sqlite:///{BASE_DIR}/database.sqlite3'
    elastic_host: str = 'elasticsearch_docker'
    # uncomment to run w/o docker and comment the line above
    # elastic_host: str = 'localhost'
    elastic_port: int = 9200
    elastic_index: str = 'search_service'
    elastic_user: str = os.getenv('ELASTIC_USERNAME')
    elastic_pass: str = os.getenv('ELASTIC_PASSWORD')


settings = Settings()
