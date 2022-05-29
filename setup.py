"""
Setup file

The code is licensed under the MIT license.
"""

from setuptools import setup, find_packages

# Setup
setup(
    name='meteostat-server',
    version='0.0.11',
    author='Meteostat',
    author_email='info@meteostat.net',
    description='Run a Meteostat JSON API server anywhere.',
    url='https://github.com/meteostat/meteostat-server',
    keywords=['weather', 'climate', 'data', 'timeseries', 'meteorology', 'json', 'api'],
    python_requires='>=3.5.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'meteostat==1.6.1',
        'configparser',
        'sqlalchemy',
        'mysql-connector-python'
    ],
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
