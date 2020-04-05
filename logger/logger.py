import logging
import os
import sys


def get_logger():
    return LoggingWrapper.__call__().get_logger()


class _LessThanFilter(logging.Filter):  # pylint: disable=R0903

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
            cls._instances[cls] = super(
                SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LoggingWrapper(object, metaclass=SingletonType):  # pylint: disable=R0903
    _logger = None

    def __init__(self):
        formatter = logging.Formatter(
            fmt='%(levelname)s|%(name)s|%(filename)s:%(lineno)s|%(funcName)s| %(message)s')

        # Get the root logger
        self._logger = logging.getLogger()

        # Note that the root logger is created with level WARNING
        self._logger.setLevel(logging.NOTSET)

        std_out = logging.StreamHandler(sys.stdout)
        # Read LOG_LEVEL from environment; default to INFO
        log_level: str = os.environ.get("LOG_LEVEL", "INFO")
        if log_level.upper() == "DEBUG":
            std_out.setLevel(logging.DEBUG)
        else:
            std_out.setLevel(logging.INFO)
        # Filter all messages below WARNING level
        std_out.addFilter(_LessThanFilter(logging.WARNING))
        std_out.setFormatter(formatter)
        self._logger.addHandler(std_out)

        std_err = logging.StreamHandler(sys.stderr)
        std_err.setLevel(logging.WARNING)
        std_err.setFormatter(formatter)
        self._logger.addHandler(std_err)

    def get_logger(self):
        return self._logger
