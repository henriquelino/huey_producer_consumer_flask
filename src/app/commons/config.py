import logging
import sys
from pathlib import Path

import yaml
from huey import SqliteHuey

logger = logging.getLogger(__name__)

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

db_path = Path(configfile['task_database']).resolve()

logger.critical(f"Using database in {db_path}")
huey = SqliteHuey(filename=str(db_path))
