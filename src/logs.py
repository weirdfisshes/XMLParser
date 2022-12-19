import sys
import logging
from logging import StreamHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = StreamHandler(stream=sys.stdout)

formatter = logging.Formatter('time: %(asctime)s, module: %(module)s, level: %(levelname)s, message: %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
