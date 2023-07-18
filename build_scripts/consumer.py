import os
import shutil
import subprocess
import sys
from pathlib import Path

import pyinstaller_versionfile

BASE_DIR = Path('.').resolve()

sys.path.append(str(BASE_DIR))
from src.app.consumer.config import __version__


def pack_code(
        license_file: str,
        input_file: str,
        output_name: str,
        base_dir: str,
        version_file_path: str,
        output_dir: str
        ):
    
    # remove exe from output name if any
    if output_name.endswith('.exe'):
        output_name.replace('.exe', '')
        
    cmd = [
        'pyarmor', 'pack',
        '--clean',
        '--name', f'{output_name}_{__version__}.exe',
        '--output', f'{output_dir}',
        '--options', f'''
            --onefile
            --noupx
            --version-file '{version_file_path}'
            --paths '{base_dir}/src/app'
            --paths '{base_dir}/src/app/consumer'
            --add-data '{base_dir}/src/app/consumer/templates/*;templates'
        ''',
        '--xoptions', '''
            --recursive
        ''',
        '--with-license', license_file,        
        input_file
    ]
    
    # normalize path separator
    cmd = [c.replace('\\', '/').replace('/', os.sep) for c in cmd] 
    
    try:
        subprocess.run(cmd, check=True)
        print('Code packed successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Error packing code: {e}')

def create_license(output_dir, name):
    
    cmd = [
        'pyarmor', 'licenses',
        '--output', output_dir, #'./licenses/',
        '--expired', '2030-01-01',
        name
    ]
    try:
        subprocess.run(cmd, check=True)
        print('License created successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Error creating license: {e}')

def main():
    license_name = 'default'
    output_name = 'consumer'

    metadata_input_file = BASE_DIR / 'producer_metadata.yaml'
    input_file =  BASE_DIR / 'src' / 'app' /'consumer'/ 'main.py'
    config_file = input_file.parent.parent / 'config.yaml'


    package_output_dir = BASE_DIR / 'deployed' / 'consumer'
    version_file = BASE_DIR / 'versionfile.txt'
    license_path = BASE_DIR / 'licenses' / license_name / 'license.lic'

    # --------------------------------------------------

    # create an version file with metadata info
    pyinstaller_versionfile.create_versionfile_from_input_file(
        output_file=version_file,
        input_file=metadata_input_file,
        version=__version__
    )

    # create a new license
    create_license(license_path.parent.parent, license_name)

    # pack the code
    pack_code(
        str(license_path),
        str(input_file),
        output_name,
        str(BASE_DIR),
        str(version_file),
        str(package_output_dir)
    )

    # copy config file too
    shutil.copy(
        config_file,
        package_output_dir / config_file.name
    )

    # cleanup
    if version_file.exists():
        version_file.unlink()
    
    return

if __name__ == '__main__':
    main()
