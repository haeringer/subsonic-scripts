import const
import logging


logging.basicConfig(
    filename=const.LOGFILE,
    level=const.LOGLEVEL,
    format='[%(asctime)s][%(levelname)s] %(message)s'
)
log = logging.getLogger()
