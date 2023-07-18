import sys
from pathlib import Path

from configjy import ConfigFile

from huey import SqliteHuey

# --------------------------------------------------

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):  # pragma: no cover
    # if it is an .exe package
    IS_EXE = True
    BASE_DIR = Path(sys.executable).parent
else:
    IS_EXE = False
    BASE_DIR = Path(__file__).parent

if IS_EXE:
    # load config file from the same folder of the executable
    configfile = ConfigFile(BASE_DIR)
else:
    # load config file from upper folder, this is the commons folder
    configfile = ConfigFile(BASE_DIR.parent)

huey = SqliteHuey(filename=configfile.get('task_database', raise_when_not_exists=True))
