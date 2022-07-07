import logging
import sys

from colorlog import ColoredFormatter
from config import LOG_LEVEL
from pythonjsonlogger import jsonlogger


def setup_logging(is_json_logs: bool = False):

    if is_json_logs:
        format_str = '%(levelname)%(message)%(asctime)%(exc_info)'
        log_handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(format_str)
        log_handler.setFormatter(formatter)
        logging.basicConfig(
            level=LOG_LEVEL,
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S:%f',
            handlers=[log_handler],
        )
        return

    colored_formatter = ColoredFormatter(
        "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%',
    )

    colored_handler = logging.StreamHandler()
    colored_handler.setFormatter(colored_formatter)

    logging.basicConfig(
        level=LOG_LEVEL,
        handlers=[colored_handler],
    )
