import logging, pytz
from fastapi.logger import logger
# from datetime import datetime
from icecream.icecream import IceCreamDebugger
from limeutils import Red

from .exceptions import *
from .settings import settings  # Not "s" let the user do the renaming
# from .cache import *
# from .app import *




# Icecream
ic = IceCreamDebugger()
ic.enabled = settings.DEBUG

# Redis
red = Red(**settings.CACHE_CONFIG.get('default'))


# Logger
# tz = pytz.timezone('Asia/Manila')
# filename = datetime.now(tz=tz).strftime(f'{s.APPCODE.upper()}:{s.ENV.lower()}-%Y-%m-%d')

warning_handler = logging.FileHandler(f'app/logs/warning.log')
warning_handler.setLevel(logging.WARNING)
file_format = '[%(asctime)s] %(levelname)s %(funcName)s:%(lineno)d: %(message)s'
warning_handler.setFormatter(logging.Formatter(file_format))
logger.addHandler(warning_handler)

critical_handler = logging.FileHandler(f'app/logs/critical.log')
critical_handler.setLevel(logging.CRITICAL)
file_format = '[%(asctime)s] %(levelname)s %(funcName)s:%(lineno)d: %(message)s'
critical_handler.setFormatter(logging.Formatter(file_format))
logger.addHandler(critical_handler)