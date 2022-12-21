import logging
import time
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def backoff(start_sleep_time: float = 0.1, factor: float = 2,
            border_sleep_time: float = 10,
            verbose: logger = logger) -> Callable:
    """
    Функция для повторного выполнения функции через некоторое время,
    если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor)
    до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param verbose: 
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            n = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    verbose.error(ex)
                    if sleep_time >= border_sleep_time:
                        sleep_time = border_sleep_time
                    else:
                        if sleep_time < border_sleep_time:
                            sleep_time = start_sleep_time * factor ** n
                        time.sleep(sleep_time)
                        n += 1

        return inner

    return func_wrapper
