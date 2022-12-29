from pydantic import (BaseSettings, Field)
import dotenv

dotenv.load_dotenv()


class Dsn(BaseSettings):
    dbname: str = Field(env='DB_NAME')
    user: str = Field(env='DB_USER')
    password: str = Field(env='DB_PASSWORD')
    host: str = Field(env='DB_HOST')
    port: str = Field(env='DB_PORT')


class EsBaseUrl(BaseSettings):
    """
    определяет host и port у ElasticSearch
    """
    es_host: str = Field(env='ES_HOST')
    es_port: str = Field(env='ES_PORT')

    def get_url(self):
        '''
        возвращает url ElasticSearch
        '''
        return 'http://{}:{}'.format(self.es_host, self.es_port)


class BaseConfig(BaseSettings):
    chunk_size: int = Field(100, env='CHUNK_SIZE')
    sleep_time: float = Field(60.0, env='ETL_SLEEP')
    es_base_url: str = EsBaseUrl().get_url()
    dsn: dict = Dsn().dict()
