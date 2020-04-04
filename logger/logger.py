import os
import logging
from logging.config import dictConfig


def get_logger():
    return LoggingWrapper.__call__().get_logger()


class _LessThanFilter(logging.Filter):

    def __init__(self, exclusive_maximum, name=""):
        super(_LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        # non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LoggingWrapper(object, metaclass=SingletonType):
    _logger = None
    _config = {
        "version": 1,
        "filters": {
            "LessThanFilter": {
                "()": _LessThanFilter,
                "exclusive_maximum": logging.ERROR
            }
        },
        "handlers": {
            "stdout": {
                "level": "DEBUG",
                "stream": "ext://sys.stdout",
                "class": "logging.StreamHandler",
                "formatter": "precise",
                "filters": ["LessThanFilter"]
            },
            "stderr": {
                "level": "ERROR",
                "stream": "ext://sys.stderr",
                "class": "logging.StreamHandler",
                "formatter": "precise",
            },
        },
        "loggers": {"console": {"handlers": ["stdout", "stderr"]}},
        "formatters": {
            "precise": {
                "format": "%(levelname)s|%(name)s|%(filename)s:%(lineno)s|%(funcName)s| %(message)s"
            }
        },
        "root": {"handlers": ["stdout", "stderr"], "level": os.environ.get("LOG_LEVEL", "INFO")},
    }

    def __init__(self):
        dictConfig(self._config)
        self._logger = logging.getLogger()

    def get_logger(self):
        return self._logger
