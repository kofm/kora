import os

DEV = os.getenv('DEV')

if DEV == '1':
    from .dev import *
