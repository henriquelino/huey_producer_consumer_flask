import logging
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional

import pyinstaller_versionfile


def build(
    version: str,
    version_file: Path,
    metadata_input_file: Path,
    license_path: Path,
    license_name: str,
    output_name: str,
    input_file: Path,
    config_file: Path,
    package_output_dir: Path,
    pyinstaller_args: Optional[List[str]] = None,
):
    if pyinstaller_args is None:
        pyinstaller_args = []

    # create an version file with metadata info
    pyinstaller_versionfile.create_versionfile_from_input_file(
        output_file=version_file,
        input_file=metadata_input_file,
        version=version,
    )

    # create a new license
    create_license(
        license_path.parent.parent,
        license_name,
    )

    # pack the code
    pack_code(
        output_name,
        str(license_path),
        str(input_file),
        str(version_file),
        str(package_output_dir),
        pyinstaller_args,
    )

    # copy config file too
    shutil.copy(
        config_file,
        package_output_dir / config_file.name,
    )

    # cleanup
    version_file.unlink(missing_ok=True)

    return


def pack_code(
    output_name: str,
    license_file: str,
    input_file: str,
    version_file_path: str,
    output_dir: str,
    additional_args: Optional[List[str]] = None,
):
    if additional_args is None:
        additional_args = []

    # remove exe from output name if any
    if not output_name.endswith('.exe'):
        output_name += '.exe'

    options = []
    options.extend(additional_args)
    options.append('--noupx')
    options.append('--onefile')
    options.append(f"--version-file '{version_file_path}'")
    options = ' '.join(options)

    x_options = []
    x_options.append('--recursive')
    x_options = ' '.join(x_options)

    # cmd break without this trailing space
    options += ' '
    x_options += ' '

    cmd = [
        'pyarmor', 'pack',
        '--clean',
        '--name', output_name,
        '--output', output_dir,
        '--options', options,
        '--xoptions', x_options,
        '--with-license', license_file,
        input_file
    ]  # yapf: disable

    try:
        subprocess.run(cmd, check=True)
        logging.critical('Code packed successfully.')
    except subprocess.CalledProcessError as e:
        logging.critical(f'Error packing code: {e}')


def create_license(
    output_dir,
    name,
):

    cmd = [
        'pyarmor', 'licenses',
        '--output', output_dir,  # './licenses/',
        '--expired', '2030-01-01',
        name
    ]  # yapf: disable
    logging.critical(cmd)
    try:
        subprocess.run(cmd, check=True)
        logging.critical('License created successfully.')
    except subprocess.CalledProcessError as e:
        logging.critical(f'Error creating license: {e}')
