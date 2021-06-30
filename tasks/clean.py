"""
Meteostat JSON API Server

The code is licensed under the MIT license.
"""

from meteostat import Hourly, Daily, Monthly, Normals

# Clear hourly cache
Hourly.clear_cache(60 * 60 * 3)

# Clear daily cache
Daily.clear_cache(60 * 60 * 48)

# Clear monthly cache
Monthly.clear_cache(60 * 60 * 24 * 30)

# Clear normals cache
Normals.clear_cache(60 * 60 * 24 * 30)
