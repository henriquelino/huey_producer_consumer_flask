__version__ = "0.1.0"

import sys
from pathlib import Path

from flask import Flask
from huey.consumer_options import ConsumerConfig
from loguru import logger  # noqa: F401
from models import STATE_MACHINE
from routes.control import controls_bp

# add the upper folder to python path to be able to import commons
sys.path.append(str(Path(__file__).resolve().parent.parent))
from commons.config import IS_EXE, configfile, huey
from commons.log import setup_logging
from commons.tasks.example import *  # noqa: F401, F403

# --------------------------------------------------


def create_flask_app() -> Flask:

    if IS_EXE:
        assets_dir = Path(sys._MEIPASS).resolve() / "assets"
    else:
        assets_dir = Path(__file__).parent / "assets"

    app = Flask('Consumer', template_folder=str(assets_dir / 'templates'))

    app.register_blueprint(controls_bp)
    return app


def main():
    setup_logging(Path(__file__).parent, **configfile.get('log', {}))

    # --------------------------------------------------
    # configure huey
    config = ConsumerConfig(**configfile.get('consumer_options', {}))
    config.validate()

    # add callbacks to state changes
    STATE_MACHINE.machine.get_transitions('start')[0].after = [STATE_MACHINE.start_consumer(huey, config.values)]
    STATE_MACHINE.machine.get_transitions('stop')[0].after = [STATE_MACHINE.stop_consumer]

    if configfile.get('consume_on_start', True) is True:
        STATE_MACHINE.start()

    # --------------------------------------------------

    app = create_flask_app()

    flask_config: dict = configfile['flask']
    flask_config['host'] = flask_config.get('host', '0.0.0.0')
    flask_config['port'] = flask_config.get('port', '5500')
    flask_config['debug'] = flask_config.get('debug', True)
    flask_config['use_reloader'] = flask_config.get('use_reloader', False)

    if IS_EXE:
        flask_config['debug'] = False

    app.run(**flask_config)
    return


if __name__ == '__main__':
    main()
