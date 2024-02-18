import random

import requests
from huey import crontab
from huey.api import Result
from loguru import logger

from commons.config import huey


@huey.task(retries=5, context=True)
def get_url(url, **kwargs) -> Result:
    logger.debug(f"{kwargs['task'].__dict__ = }")

    # --------------------------------------------------

    task_data = kwargs['task']
    task_id = task_data.id
    retries_left = task_data.retries

    # --------------------------------------------------

    logger.info(f"\n{'-'*60}\n\tNEW TASK INCOMING! -> id='{task_id}'; Retries left='{retries_left}'\n'{url = }'\n{kwargs = }\n{'-'*60}")

    # --------------------------------------------------

    if retries_left > 0 and random.randint(0, 5) > 1:
        raise Exception(f"\n{'-'*60}\nRETRYING\n{'-'*60}\n\n\n")

    r = requests.get(url)
    r.raise_for_status()

    # --------------------------------------------------

    logger.info(f"[{task_id}] done!\n{'-'*60}")
    return r


@huey.periodic_task(crontab(minute='*'), context=True)
def every_minute(**kwargs):
    logger.debug(f"{kwargs['task'].__dict__ = }")

    logger.info("This task runs every minute")

    huey.put('every_minute__return', True)
    return
