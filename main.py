import logging
import os
import sys

from const import *

# Init logging
log = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)

# Mandatory environment variables
if not all(
        [
            os.environ.get("SSO_COOKIE"),
            os.environ.get("PLAYSTATION_USERID"),
        ]
):
    log.error("Missing or empty configuration variables.")

