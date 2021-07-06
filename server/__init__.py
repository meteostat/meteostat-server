"""
Official Meteostat JSON API Server

The code is licensed under the MIT license.
"""

__appname__ = 'server'
__version__ = '0.0.8'

from flask import Flask, request
from .utils import get_config

# Create Flask app instance
app = Flask(__name__)

# Get configuration
config = get_config()

# Check secret header
@app.before_request
def secret():
    # Get header name
    name = config.get('secret', 'name')
    # Get header value
    value = config.get('secret', 'value')
    # Get header
    if request.headers.get(name) != value:
        # Unauthorized
        abort(401)

@app.after_request
def poweredby(resp):
    resp.headers['X-Meteostat-Server'] = config.get("server", "name")
    return resp

# Import API endpoints
from .endpoints.stations.meta import *
from .endpoints.stations.nearby import *
from .endpoints.stations.hourly import *
from .endpoints.stations.daily import *
from .endpoints.stations.monthly import *
from .endpoints.stations.normals import *
from .endpoints.point.hourly import *
from .endpoints.point.daily import *
from .endpoints.point.monthly import *
from .endpoints.point.normals import *
