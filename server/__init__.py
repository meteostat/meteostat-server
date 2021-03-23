
"""
Official Meteostat JSON API

The code is licensed under the MIT license.
"""

__appname__ = 'server'
__version__ = '0.0.1'

from flask import Flask

# Create Flask app instance
app = Flask(__name__)

# Import API endpoints
from .point import hourly as point_hourly
from .point import daily as point_daily
from .station import hourly as station_hourly
from .station import daily as station_daily
