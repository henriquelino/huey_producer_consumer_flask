import os
import sys
from pathlib import Path

# expand python path so modules can import as if running on terminal/exe
sys.path.append(str(Path('.').resolve()))
sys.path.append(str(Path('.').resolve() / 'src'))
sys.path.append(str(Path('.').resolve() / 'src' / 'consumer'))
sys.path.append(str(Path('.').resolve() / 'src' / 'producer'))

if sys.platform == "win32":
    # without this tox couldn't find chrome binary, if using selenium
    os.environ.update({"PROGRAMW6432": "C:\\Program Files"})
