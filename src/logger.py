import logging
from sys import stdout

stream_handler = logging.StreamHandler(stream=stdout)
log_handler = logging.FileHandler("./logs.log")
logging.basicConfig(
    level=logging.INFO,
    handlers=(stream_handler, log_handler),
    format="[%(levelname)s]: %(message)s, %(name)s, %(asctime)s",
)
logger = logging.getLogger(__name__)
