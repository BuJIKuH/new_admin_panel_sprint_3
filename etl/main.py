import datetime
import logging
import time
import backoff
import elasticsearch
import psycopg2

from ETL_classes.extractor import Extractor
from ETL_classes.loader import Loader
from ETL_classes.transformer import Transformer

from state import (State, JsonFileStorage)
from utils.settings_etl import BaseConfig
from utils.logger_etl import get_logger


@backoff.on_exception(wait_gen=backoff.expo, exception=(
    elasticsearch.exceptions.ConnectionError))
@backoff.on_exception(wait_gen=backoff.expo,
                      exception=(psycopg2.Error, psycopg2.OperationalError))
def etl(verbose: logging.Logger,
        extractor: Extractor,
        transformer: Transformer,
        state: State,
        loader: Loader) -> None:
    '''
    ETL процесс перекачки данных из PostgresSQL в Elasticsearch
    '''

    last_sync_timestamp = state.get_state('last_sync_timestamp')
    verbose.info(f'последняя синхронизация была {last_sync_timestamp}')
    start_timestamp = datetime.datetime.now()
    for extracted_part in extractor.extract(
        last_sync_timestamp
    ):
        data = transformer.transform(extracted_part)
        loader.load(data)
        state.set_state("last_sync_timestamp", str(start_timestamp))


if __name__ == '__main__':
    configs = BaseConfig()
    logger = get_logger(__name__)
    state = State(JsonFileStorage(file_path='state.json'))
    extractor = Extractor(psql_dsn=configs.dsn, chunk_size=configs.chunk_size,
                          storage_state=state, verbose=logger)
    transformer = Transformer()
    loader = Loader(dsn=configs.es_base_url, verbose=logger)

    while True:
        etl(logger, extractor, transformer, state, loader)
        logger.info(f'Засыпаю на {configs.sleep_time}')
        time.sleep(configs.sleep_time)
