import sys
from pathlib import Path

from huey.api import Result  # noqa: F401

sys.path.append(str(Path('.').resolve().parent))
import consumer.tasks.example as tasks

def main():
    # create some tasks to just open an url
    # in reality we would generate tasks from an database
    # just sending the PK of the task
    # so the producer is an extremely simple script
    urls = [
        'https://github.com/henriquelino/selenium_tkit',
        'https://github.com/henriquelino',
        'https://github.com/henriquelino/autohotkey',
        'https://github.com/henriquelino/rpachallenge',
        'https://github.com/henriquelino/configjy',
    ]
    for url in urls:
        print('creating task')
        tasks.open_an_url(url)
    return

if __name__ == '__main__':
    main()