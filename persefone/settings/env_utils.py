import os


def getenv_bool(var, default=False):
    val = os.getenv(var)
    if val is None:
        return default
    return val.strip().lower() in ("true", "1", "yes", "on")


def getenv_list(var, default=()):
    val = os.getenv(var)
    return val.split() if val else default
