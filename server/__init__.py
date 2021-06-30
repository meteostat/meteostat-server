
"""
Official Meteostat JSON API Server

The code is licensed under the MIT license.
"""

__appname__ = 'server'
__version__ = '0.0.7'

import os
from configparser import ConfigParser
from flask import Flask, request

# Create Flask app instance
app = Flask(__name__)

# Path of configuration file
config_path: str = os.path.expanduser(
    '~') + os.sep + '.meteostat-server' + os.sep + 'config.ini'

# Get configuration
config = ConfigParser()
config.read(config_path)

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

# Import API endpoints
from .endpoints.point.hourly import *
from .endpoints.point.daily import *
from .endpoints.stations.hourly import *
from .endpoints.stations.daily import *
