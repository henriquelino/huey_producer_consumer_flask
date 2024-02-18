import sys
from pathlib import Path

from helpers import build

BASE_DIR = Path(__file__).parent.parent.resolve()
SRC_DIR = BASE_DIR / 'src'

sys.path.append(str(SRC_DIR / 'producer'))  # to include folders like 'models
sys.path.append(str(BASE_DIR))
from src.producer.main import __version__


def main():
    license_name = 'default_producer'
    output_name = f'producer_{__version__}.exe'

    metadata_input_file = BASE_DIR / 'metadata_producer.yaml'
    input_file = SRC_DIR / 'producer' / 'main.py'
    config_file = input_file.parent.parent / 'config.yaml'

    package_output_dir = BASE_DIR / 'deployed' / 'producer'
    version_file = BASE_DIR / 'versionfile_producer.txt'
    license_path = BASE_DIR / 'licenses' / license_name / 'license.lic'

    pyinstaller_args = []
    pyinstaller_args.append(f"--paths '{BASE_DIR / 'src' }'")  # so we can import from commons
    pyinstaller_args.append(f"--paths '{BASE_DIR / 'src' / 'producer'}'")  # so we can import from producer dir

    # --------------------------------------------------

    build(
        version=__version__,
        version_file=version_file,
        metadata_input_file=metadata_input_file,
        license_path=license_path,
        license_name=license_name,
        output_name=output_name,
        input_file=input_file,
        config_file=config_file,
        package_output_dir=package_output_dir,
        pyinstaller_args=pyinstaller_args
    )

    return


if __name__ == '__main__':
    main()
