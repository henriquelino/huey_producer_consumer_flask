__version__ = '0.1.0'

import sys
from pathlib import Path

from huey.api import Result  # noqa: F401
from loguru import logger

# add the upper folder to python path to be able to import commons folder
sys.path.append(str(Path(__file__).resolve().parent.parent))

import commons.tasks as tasks
from commons import BASE_DIR, configfile
from commons.log import setup_logging


def main():
    setup_logging(BASE_DIR, **configfile.get('log', {}))
    # create some tasks to just open an url
    # in reality we would generate tasks from an database
    # just sending the PK of the task
    # so the producer is an extremely simple script
    urls = [
        'https://github.com/henriquelino/selenium_tkit',
        'https://github.com/henriquelino',
        'https://github.com/henriquelino/autohotkey',
        'https://github.com/henriquelino/rpachallenge',
    ]
    logger.info(f'creating {len(urls)} tasks')
    tasks.get_url.map(urls)

    logger.info('creating 1 more task')
    tasks.get_url('https://github.com/henriquelino/configjy')

    return


if __name__ == '__main__':
    main()
