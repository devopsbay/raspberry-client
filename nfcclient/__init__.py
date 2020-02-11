from .config import ClientConfig
from .nfc_reader import *

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.getLogger(__name__).setLevel(logging.INFO)



__version__ = "0.0.1"
