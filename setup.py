"""
Setup file

The code is licensed under the MIT license.
"""

from os import path
from setuptools import setup, find_packages

# Content of the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

# Setup
setup(
    name='meteostat-server',
    version='0.0.5',
    author='Meteostat',
    author_email='info@meteostat.net',
    description='Run a Meteostat JSON API server anywhere.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/meteostat/meteostat-server',
    keywords=['weather', 'climate', 'data', 'timeseries', 'meteorology', 'json', 'api'],
    python_requires='>=3.5.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['flask', 'meteostat==1.5.1'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
         'Topic :: Database',
         'Topic :: Scientific/Engineering :: Atmospheric Science',
         'Topic :: Scientific/Engineering :: Information Analysis',
    ],
)
