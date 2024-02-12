import logging
import shutil
import subprocess
from pathlib import Path

import pyinstaller_versionfile


def build(
    version,
    version_file: Path,
    metadata_input_file,
    license_path: Path,
    license_name,
    output_name,
    input_file,
    base_dir,
    config_file: Path,
    package_output_dir,
):

    # create an version file with metadata info
    pyinstaller_versionfile.create_versionfile_from_input_file(output_file=version_file, input_file=metadata_input_file, version=version)

    # create a new license
    create_license(license_path.parent.parent, license_name)

    # pack the code
    pack_code(output_name, str(license_path), str(input_file), base_dir, str(version_file), str(package_output_dir))

    # copy config file too
    shutil.copy(config_file, package_output_dir / config_file.name)

    # cleanup
    version_file.unlink(missing_ok=True)

    return


def pack_code(output_name: str, license_file: str, input_file: str, base_dir: Path, version_file_path: str, output_dir: str):

    # remove exe from output name if any
    if not output_name.endswith('.exe'):
        output_name += '.exe'

    cmd = [
        'pyarmor', 'pack', '--clean', '--name', output_name, '--output', output_dir, '--options', f"""
            --onefile
            --noupx
            --version-file '{version_file_path}'
            --paths '{str(base_dir / 'src' / 'app')}'
            --paths '{str(base_dir / 'src' / 'app' / 'consumer')}'
            --paths '{str(base_dir / 'src' / 'app' / 'producer')}'
        """, '--xoptions', '''
            --recursive
        ''', '--with-license', license_file, input_file
    ]

    # normalize path separator
    # cmd = [c.replace('\\', '/').replace('/', os.sep) for c in cmd]

    try:
        subprocess.run(cmd, check=True)
        logging.critical('Code packed successfully.')
    except subprocess.CalledProcessError as e:
        logging.critical(f'Error packing code: {e}')


def create_license(output_dir, name):

    cmd = [
        'pyarmor',
        'licenses',
        '--output',
        output_dir,  # './licenses/',
        '--expired',
        '2030-01-01',
        name
    ]
    logging.critical(cmd)
    try:
        subprocess.run(cmd, check=True)
        logging.critical('License created successfully.')
    except subprocess.CalledProcessError as e:
        logging.critical(f'Error creating license: {e}')
