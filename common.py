import os
import logging


VERSION = os.environ.get('SSC_APIVERSION')
SERVER = os.environ.get('SSC_SERVER').rstrip('/')
USER = os.environ.get('SSC_USER')
PASSWD = os.environ.get('SSC_PASSWD')

CLIENT = 'subsonic_scripts'

LOGLEVEL = os.environ.get('SSC_LOGLEVEL', 'INFO')
LOGFILE = os.environ.get('SSC_LOGFILE', '/var/log/subsonic_playlists_dedup')

logging.basicConfig(
    filename=LOGFILE,
    level=LOGLEVEL,
    format='[%(asctime)s][%(levelname)s] %(message)s'
)
log = logging.getLogger()
