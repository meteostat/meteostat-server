
"""
Official Meteostat JSON API

The code is licensed under the MIT license.
"""

__appname__ = 'meteostat-server'
__version__ = '0.0.1'

from flask import Flask

# Create Flask app instance
app = Flask(__name__)

# Import API endpoints
from server.station import hourly as station_hourly
from server.station import daily as station_daily
from server.point import hourly as point_hourly
from server.point import daily as point_daily
