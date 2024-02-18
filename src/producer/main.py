__version__ = '0.1.0'

import json
import sys
from pathlib import Path
from typing import List

from huey.api import Result, ResultGroup  # noqa: F401
from loguru import logger

# add the upper folder to python path to be able to import commons folder
sys.path.append(str(Path(__file__).resolve().parent.parent))

import commons.tasks as tasks
from commons.config import IS_EXE, configfile
from commons.log import setup_logging

# --------------------------------------------------

BASE_DIR = Path(sys.executable).resolve().parent if IS_EXE else Path('.').resolve()


def jsondefault(v):
    try:
        return v.__dict__
    except:  # noqa: E722
        return str(v)


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
    created_tasks: List[Result] = []

    logger.info(f'creating {len(urls)} tasks')
    resultgroup: ResultGroup = tasks.get_url.map(urls)
    created_tasks.extend(i for i in resultgroup)

    logger.info('creating 1 more task')
    r: Result = tasks.get_url('https://github.com/henriquelino/configjy')

    created_tasks.append(r)

    logger.info(f"Created tasks metadata: {json.dumps(created_tasks, indent=2, default=jsondefault)}")

    return


if __name__ == '__main__':
    main()
