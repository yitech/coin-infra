import logging
import os
import threading


class CustomLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pid = os.getpid()
        self.tid = threading.get_ident()


class LoggerConfig:
    log_format = '[%(asctime)s.%(msecs)03d][%(pid)s][%(tid)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_format, date_format)

    @classmethod
    def get_log_path(cls, log_dir, *names) -> str:
        log_file = f"{'_'.join(names)}.log"
        return os.path.join(log_dir, log_file)

    @classmethod
    def setup_logger(cls, log_dir, *names, level=logging.INFO) -> logging.Logger:
        logger = logging.getLogger('_'.join(names))

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(cls.formatter)
        logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(cls.get_log_path(log_dir, *names))
        file_handler.setFormatter(cls.formatter)
        logger.addHandler(file_handler)

        logger.setLevel(level)
        logger.info(f"Initialize {'_'.join(names)}")

        return logger


class FilePathUtil:
    @staticmethod
    def get_filename(path: str) -> str:
        return os.path.splitext(os.path.basename(path))[0]


# Initializing the custom log record factory
logging.setLogRecordFactory(CustomLogRecord)
