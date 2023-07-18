import os
from pathlib import Path
import sys


sys.path.append(str(Path('.').resolve() / 'src' / 'app'))
if sys.platform == "win32":
    # without this tox couldn't find chrome binary
    os.environ.update({"PROGRAMW6432": "C:\\Program Files"})
