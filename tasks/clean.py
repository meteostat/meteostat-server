"""
Meteostat JSON API Server

The code is licensed under the MIT license.
"""

from meteostat import Hourly, Daily, Monthly, Normals

# Change cache directory to Apache user
cache_dir = '/var/www/.meteostat/cache'
Hourly.cache_dir = cache_dir
Daily.cache_dir = cache_dir
Monthly.cache_dir = cache_dir
Normals.cache_dir = cache_dir

# Clear hourly cache
Hourly.clear_cache(60 * 60 * 3)

# Clear daily cache
Daily.clear_cache(60 * 60 * 48)

# Clear monthly cache
Monthly.clear_cache(60 * 60 * 24 * 30)

# Clear normals cache
Normals.clear_cache(60 * 60 * 24 * 30)
