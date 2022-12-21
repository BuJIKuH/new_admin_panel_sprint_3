import os

from dotenv import load_dotenv
from pydantic import BaseConfig, Field

load_dotenv()


class PostgresSettings(BaseConfig):
    dbname: str = Field(os.environ.get('DB_NAME'))
    user: str = Field(os.environ.get('DB_USER'))
    password: str = Field(os.environ.get('DB_PASSWORD'))
    host: str = Field(os.environ.get('DB_HOST'))
    port: str = Field(os.environ.get('DB_PORT'))
    options: str = '-c search_path=content'


class ElasticSearchSettings(BaseConfig):
    host: str = Field(os.environ.get('ES_HOST'))
    index: str = Field(os.environ.get('ES_INDEX'))
