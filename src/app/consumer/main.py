__version__ = "0.1.0"

import sys
import threading
import time
from pathlib import Path

from flask import Flask
from huey.consumer_options import ConsumerConfig
from loguru import logger  # noqa: F401
from models.ConsumerState import CONSUMER_STATE
from routes.control import controls_bp

# add the upper folder to python path to be able to import commons
sys.path.append(str(Path(__file__).resolve().parent.parent))
from commons.config import BASE_DIR, IS_EXE, configfile, huey
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
    setup_logging(BASE_DIR, **configfile.get('log', {}))

    app = create_flask_app()

    flask_config: dict = configfile['flask']
    flask_config['host'] = flask_config.get('host', '0.0.0.0')
    flask_config['port'] = flask_config.get('port', '5500')
    flask_config['debug'] = flask_config.get('debug', True)

    if IS_EXE:
        # dont run in debug mode if is an .exe even if config file told to
        flask_config['debug'] = False

    # as we are running flask in another thread, we cant use reloader
    flask_config['use_reloader'] = False

    app_thread = threading.Thread(target=lambda: app.run(**flask_config))
    app_thread.daemon = True
    app_thread.start()
    logger.critical(f"Flask server is running @ '{flask_config['host']}:{flask_config['port']}'")

    # --------------------------------------------------
    # configure huey
    config = ConsumerConfig(**configfile.get('consumer_options', {}))
    config.validate()

    # --------------------------------------------------

    # change state if we should boot already consuming
    if configfile.get('consume_on_start', False):
        CONSUMER_STATE.state = CONSUMER_STATE.States.running

    # handle huey and flask /start /stop
    # reminder: state changes are handled in routes
    running = False
    while True:

        if CONSUMER_STATE.state == CONSUMER_STATE.States.running and not running:
            # if the state is for running and we aren't, then we should start the consumer
            consumer = huey.create_consumer(**config.values)
            consumer.start()
            running = True

        elif CONSUMER_STATE.state == CONSUMER_STATE.States.stopped and running:
            # if the state is stopped and we are running, we should stop the consumer
            consumer.stop(graceful=True)
            running = False

        else:
            # if the state didn't change, we do nothing and wait for a second
            time.sleep(1)


if __name__ == '__main__':
    main()
