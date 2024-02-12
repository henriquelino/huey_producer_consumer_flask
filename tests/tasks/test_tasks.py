import requests
from huey.api import Result
from loguru import logger  # noqa: F401

from src.app.commons import huey
from src.app.commons.tasks import every_minute, get_url


class TestTasks:

    @classmethod
    def setup_class(cls):
        huey.immediate = True

    def test__get_url(self):
        # idk why this should run with huey.enqueue, without it the function never runs
        # as this task use context, cant run raw function with get_url.func(...)
        r: Result = huey.enqueue(get_url.s('https://www.google.com'))
        r = r.get(blocking=True, timeout=10)
        assert isinstance(r, requests.Response) is True

    def test__every_minute(self):
        # this function does not use context, but are periodic, so I couldnt run with huey.enqueue and get its return
        r = every_minute.func()
        assert r is None
