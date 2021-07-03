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

# Max. cache time
max_cache_time = 60 * 60 * 24 * 30

# Clear hourly cache
Hourly.clear_cache(max_cache_time)

# Clear daily cache
Daily.clear_cache(max_cache_time)

# Clear monthly cache
Monthly.clear_cache(max_cache_time)

# Clear normals cache
Normals.clear_cache(max_cache_time)
