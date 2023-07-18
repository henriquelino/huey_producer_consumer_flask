import sys
import threading
import time
from pathlib import Path

from config import BASE_DIR, IS_EXE, configfile, huey
from flask import Flask
from loguru import logger  # noqa: F401
from models.ConsumerState import CONSUMER_STATE, States
from routes.control import controls_bp

from huey.consumer_options import ConsumerConfig

sys.path.append(str(Path('.').resolve().parent))
from commons.log import setup_logging
# the tasks should be the last thing loaded
from consumer.tasks.example import *  # noqa: F401, F403

# --------------------------------------------------

if IS_EXE:
    templates_dir = Path(sys._MEIPASS).resolve() / "templates"
else:
    templates_dir = BASE_DIR / "templates"

# --------------------------------------------------

app = Flask('Consumer', template_folder=templates_dir)

app.register_blueprint(controls_bp)

# --------------------------------------------------


def main():
    setup_logging(BASE_DIR, **configfile.get('log', {}))

    # --------------------------------------------------
    # configure flask

    flask_config: dict = configfile.get('app', raise_when_not_exists=True)
    flask_config['host'] = flask_config.get('host', '0.0.0.0')
    flask_config['port'] = flask_config.get('port', '5500')
    flask_config['debug'] = flask_config.get('debug', True)

    if IS_EXE:
        # dont run in debug mode if is an .exe even if config file told to
        flask_config['debug'] = False

    # as we are running flask in another thread, we cant use reloader
    flask_config['use_reloader'] = False

    app_thread = threading.Thread(target=lambda: app.run(**flask_config))
    # app_thread = threading.Thread(target=app.run)
    app_thread.daemon = True
    app_thread.start()
    logger.critical(f"Flask server is running @ '{flask_config['host']}:{flask_config['port']}'")

    # --------------------------------------------------
    # configure huey
    config = ConsumerConfig(**configfile.get('consumer_options', {}))
    config.validate()

    # --------------------------------------------------
    # handle huey and flask /start /stop
    running = False
    while True:

        if CONSUMER_STATE.state == States.running and not running:
            # if the state is for running and we aren't, then we should start the consumer
            consumer = huey.create_consumer(**config.values)
            consumer.start()
            running = True

        elif CONSUMER_STATE.state == States.stopped and running:
            # if the state is stoppend and we are running, we should stop the consumer
            consumer.stop(graceful=True)
            running = False

        else:
            # if the state didn't change, we do nothing and wait for a second
            time.sleep(1)


if __name__ == '__main__':
    main()
