import sys
from pathlib import Path

from configjy import ConfigFile

from huey import SqliteHuey

# --------------------------------------------------

__version__ = "0.1.0.1"

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):  # pragma: no cover
    # if it is an .exe package
    IS_EXE = True
    BASE_DIR = Path(sys.executable).parent
else:
    IS_EXE = False
    BASE_DIR = Path(__file__).parent

configfile = ConfigFile(BASE_DIR)

db_path = configfile.get('task_database', raise_when_not_exists=True)
huey = SqliteHuey(filename=db_path)
