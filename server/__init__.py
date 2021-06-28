
"""
Official Meteostat JSON API Server

The code is licensed under the MIT license.
"""

__appname__ = 'server'
__version__ = '0.0.4'

from flask import Flask

# Create Flask app instance
app = Flask(__name__)

# Import API endpoints
from .point_hourly import *
from .point_daily import *
from .station_hourly import *
from .station_daily import *
