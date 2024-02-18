import time

import requests
from huey.api import Result
from loguru import logger  # noqa: F401

from commons import huey
from commons.tasks import every_minute, get_url


class TestTasks:

    @classmethod
    def setup_class(cls):
        huey.immediate = True

    def test__get_url(self):
        r: Result = get_url('https://www.google.com')
        r = r.get(blocking=True, timeout=10)
        assert isinstance(r, requests.Response) is True

    def test__every_minute(self):
        # logger.debug(f"{huey._registry.__dict__ = }")
        # logger.debug(f"{huey.read_periodic(None) = }")
        # logger.debug(f"{huey.scheduled() = }")
        # logger.debug(f"{huey.scheduled_count() = }")
        # logger.debug(f"{huey.pending() = }")
        # logger.debug(f"{huey.pending_count() = }")

        r: Result = every_minute()

        begin = time.perf_counter()
        while (time.perf_counter() - begin) < 10:
            r = huey.get('every_minute__return', peek=True)
            if r is not True:
                time.sleep(1)
                continue
            break
        else:
            raise TimeoutError

        assert r is True
