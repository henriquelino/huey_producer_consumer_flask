import time

import commons.lib as lib
from commons.config import huey
from loguru import logger

from huey import crontab
from huey.api import Result


@huey.task(retries=5)
def open_an_url(url) -> Result:
    logger.info(f"NEW TASK INCOMING! -> '{url}'")
    # if random.randint(0, 5) > 1:
    #     raise Exception(f"RETRYING\n{'-'*60}\n\n\n")

    driver = lib.create_chrome()

    r = driver.open_url(url)
    if r is False:
        raise Exception(f"Could not open '{url}'")

    time.sleep(15)

    logger.info(f"done!\n{'-'*60}")
    return


@huey.periodic_task(crontab(minute='*'))
def every_minute():
    print('This task runs every minute')
