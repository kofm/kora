import os

AUTHLOG_FILE_PATH = os.getenv("AUTHLOG_FILE_PATH", "/var/log/kora/auth.log")

AUTHLOG_HANDLER = {
    "authlog_file": {
        "class": "logging.handlers.WatchedFileHandler",
        "filename": AUTHLOG_FILE_PATH,
        "level": "WARNING",
        "formatter": "login_failed",
    },
}

AUTHLOG_LOGGER = {
    "authlog.failed_login": {
        "handlers": ["authlog_file"],
        "level": "WARNING",
        "propagate": False,
    }
}

AUTHLOG_FORMATTER = {
    "login_failed": {
        "format": "{asctime} {message}",
        "style": "{",
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }
}
