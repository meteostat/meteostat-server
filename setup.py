from os import path
from setuptools import setup, find_packages

# Setup
setup(
     name = 'api',
     version = '0.1.0',
     author = 'Meteostat',
     author_email = 'info@meteostat.net',
     description = 'Meteostat JSON API.',
     url = 'https://github.com/meteostat/api',
     packages = find_packages(),
     include_package_data = True,
     install_requires = ['flask', 'pandas'],
     license = 'MIT',
     classifiers = [
         'Programming Language :: Python :: 3',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
     ],
 )
