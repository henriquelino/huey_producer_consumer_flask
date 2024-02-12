import sys
from pathlib import Path

from helpers import build

BASE_DIR = Path(__file__).parent.parent.resolve()
SRC_DIR = BASE_DIR / 'src'

sys.path.append(str(SRC_DIR / 'app' / 'consumer'))
sys.path.append(str(SRC_DIR))
from app.consumer.main import __version__


def main():
    output_name = f'consumer{__version__}.exe'

    metadata_input_file = BASE_DIR / 'metadata_consumer.yaml'
    input_file = SRC_DIR / 'app' / 'consumer' / 'main.py'
    config_file = input_file.parent.parent / 'config.yaml'

    package_output_dir = BASE_DIR / 'deployed' / 'consumer'
    version_file = BASE_DIR / 'versionfile_consumer.txt'
    license_name = 'default_consumer'
    license_path = BASE_DIR / 'licenses' / license_name / 'license.lic'

    # --------------------------------------------------

    build(
        version=__version__,
        version_file=version_file,
        metadata_input_file=metadata_input_file,
        license_path=license_path,
        license_name=license_name,
        output_name=output_name,
        input_file=input_file,
        base_dir=BASE_DIR,
        config_file=config_file,
        package_output_dir=package_output_dir,
    )

    return


if __name__ == '__main__':
    main()
