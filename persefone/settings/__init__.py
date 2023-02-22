import os

DEV = os.getenv('DEV')
SECRET_KEY = os.getenv('SECRET_KEY')

if DEV == '1':
    from .dev import *
else:
    from .prod import *
