import platform
import sys
from pathlib import Path

import yaml
from huey import SqliteHuey
from loguru import logger  # noqa: F401

# --------------------------------------------------

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):  # pragma: no cover
    # if it is an .exe package
    IS_EXE = True
    BASE_DIR = Path(sys.executable).parent
    # load config file from the same folder of the executable
    config_file_dir = BASE_DIR
else:
    IS_EXE = False
    BASE_DIR = Path(__file__).parent
    # load config file from upper folder, this should be the commons folder
    config_file_dir = BASE_DIR.parent

with (config_file_dir / 'config.yaml').open('r') as f:
    configfile: dict = yaml.safe_load(f)

# solves an issue where windows path wouldn't work in unix even using pathlib
if platform.system() != 'Windows':
    db_path = configfile['task_database'].replace('\\', '/')
else:
    db_path = configfile['task_database'].replace('/', '\\')

db_path = Path(db_path).resolve()

logger.critical(f"Using database in {db_path}")
huey = SqliteHuey(filename=str(db_path))
