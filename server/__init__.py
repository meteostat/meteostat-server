
"""
Official Meteostat JSON API

The code is licensed under the MIT license.
"""

__appname__ = 'server'
__version__ = '0.0.3'

from flask import Flask

# Create Flask app instance
app = Flask(__name__)

# Import API endpoints
import .point_hourly
import .point_daily
import .station_hourly
import .station_daily
