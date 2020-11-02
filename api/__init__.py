
"""
Official Meteostat JSON API

The code is licensed under the MIT license.
"""

from flask import Flask

# Configuration
version = '3'

# Create Flask app instance
app = Flask(__name__)

# Import API endpoints
from api import hourly
from api import daily

if __name__ == '__main__':
  app.run()
