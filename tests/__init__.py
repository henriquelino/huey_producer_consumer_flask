import os
import sys
from pathlib import Path

cwd = Path('.').resolve()
src = cwd / 'src'
sys.path.append(str(src))
sys.path.append(str(src / 'consumer'))
sys.path.append(str(src / 'producer'))
os.chdir(str(src))

if sys.platform == "win32":
    # without this tox couldn't find chrome binary, if using selenium
    os.environ.update({"PROGRAMW6432": "C:\\Program Files"})
