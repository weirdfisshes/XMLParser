import sys
import logging
from logging import StreamHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(filename)s,'
    'line %(lineno)d, in %(funcName)s, message: %(message)s'
)

handler.setFormatter(formatter)
logger.addHandler(handler)
