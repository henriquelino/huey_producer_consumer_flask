import logging
import sys
from pathlib import Path

from loguru import logger


class ThreadLogFilter(logging.Filter):
    """
    This filter only show log entries for specified thread name
    """

    def __init__(self, *args, **kwargs):
        logging.Filter.__init__(self, *args, **kwargs)

    def filter(self, record):
        print(f"{record = }")


class InterceptHandler(logging.Handler):

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(dir: Path, **kwargs):
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    LOG_LEVEL = kwargs.get("level", "DEBUG")
    logging.root.setLevel(LOG_LEVEL)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru

    log_path = Path(dir / "logs" / "{time}.log").resolve()
    if not log_path.parent.exists():
        log_path.parent.mkdir(parents=True)
        logger.critical(f"Pasta de logs: '{str(log_path.parent)}' foi criada")

    prompt_config = {'sink': sys.stderr, 'level': LOG_LEVEL}

    file_config = {
        'sink': log_path,
        'rotation': kwargs.get('rotation', "00:00"),
        'compression': kwargs.get('compression', "zip"),
        'retention': kwargs.get('retention', "30 days"),
        'level': LOG_LEVEL,
        'enqueue': True
    }

    if format := kwargs.get('format'):
        file_config['format'] = format
        prompt_config['format'] = format

    logger.remove()
    logger.add(**prompt_config)
    logger.add(**file_config)

    # logger.configure(
    #     handlers=[
    #         dict(sink=sys.stderr, level=LOG_LEVEL),

    #         dict(sink=log_path,
    #              rotation=kwargs.get('rotation', "00:00"),
    #              compression=kwargs.get('compression', "zip"),
    #              retention=kwargs.get('retention', "30 days"),
    #              level=LOG_LEVEL,
    #              enqueue=True,
    #              format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {thread.name} <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>',
    #              filter=ThreadLogFilter
    #         )
    #     ]
    # )  # yapf: disable

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)
    logging.getLogger("selenium_tkit").setLevel(logging.CRITICAL)
    logging.getLogger("werkzeug").setLevel(logging.CRITICAL)
