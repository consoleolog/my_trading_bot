import logging
import os

fmt = "[%(levelname)s] %(asctime)s : %(filename)s : %(lineno)d - %(message)s"

datefmt = '%Y-%m-%d %H:%M:%S'


class CustomFormatter(logging.Formatter):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    green = '\x1b[38;5;46m'
    bold_green = '\x1b[32;1m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.bold_green + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=datefmt)
        return formatter.format(record)


def create_file_handler(log_level, log_dir):
    file_handler = logging.FileHandler(f"{log_dir}/{log_level.lower()}.log")
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, log_level))
    return file_handler


def set_loglevel(level, log_dir='.logs'):
    try:
        if not os.path.exists(f"{os.getcwd()}/{log_dir}"):
            os.mkdir(f"{os.getcwd()}/{log_dir}")

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(CustomFormatter(fmt))
        logger.addHandler(stream_handler)

        log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        for log_level in log_levels:
            file_handler = create_file_handler(log_level, log_dir)
            logger.addHandler(file_handler)

        if level.upper() == "D":
            logger.setLevel(logging.DEBUG)
        elif level.upper() == "E":
            logger.setLevel(logging.ERROR)
        else:
            logger.setLevel(logging.INFO)

    except Exception:
        raise
