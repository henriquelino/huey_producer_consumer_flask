import os
import sys
from pathlib import Path

# expand python path so modules can import as if running on terminal/exe
sys.path.append(str(Path('.').resolve()))
sys.path.append(str(Path('.').resolve() / 'src' / 'app'))
sys.path.append(str(Path('.').resolve() / 'src' / 'app' / 'consumer'))

if sys.platform == "win32":
    # without this tox couldn't find chrome binary
    os.environ.update({"PROGRAMW6432": "C:\\Program Files"})
