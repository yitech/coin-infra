import os
import logging
import datetime
import inspect

class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s][%(levelname)s]%(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)

        self.logger.addHandler(console_handler)

    def _get_caller_info(self):
        """
        Get caller's filename and line number
        """
        frame = inspect.stack()[2]
        filename = os.path.basename(frame[1])
        line = frame[2]

        return filename, line

    def info(self, message):
        filename, line = self._get_caller_info()
        self.logger.info(f'[{filename}:{line}] {message}')

    def warning(self, message):
        filename, line = self._get_caller_info()
        self.logger.warning(f'[{filename}:{line}] {message}')

    def error(self, message):
        filename, line = self._get_caller_info()
        self.logger.error(f'[{filename}:{line}] {message}')
