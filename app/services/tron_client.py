from tronpy import Tron
from tronpy.providers import HTTPProvider
from app.core.config import TRON_NODE_URL

if TRON_NODE_URL:
    client = Tron(HTTPProvider(endpoint_uri=TRON_NODE_URL))
else:
    client = Tron()