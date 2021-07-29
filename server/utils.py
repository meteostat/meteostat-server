"""
Meteostat JSON API Server

The code is licensed under the MIT license.
"""

import os
from configparser import ConfigParser
from flask import request, Response
from sqlalchemy import create_engine, text

# Path of configuration file
config_path: str = os.path.expanduser(
    '~') + os.sep + '.meteostat-server' + os.sep + 'config.ini'

def get_config() -> ConfigParser:
    """
    Get data from configuration file
    """

    # Get configuration
    config = ConfigParser()
    config.read(config_path)

    # Return
    return config

def db_query(query: str, payload: dict = {}):
    """
    Query data from SQL database
    """

    # Get configuration
    config = get_config()

    database = create_engine(f"""mysql+mysqlconnector://{config.get('database', 'user')}:{config.get('database', 'password')}@{config.get('database', 'host')}/{config.get('database', 'name')}?charset=utf8""")

    with database.connect() as con:
        return con.execute(text(query).execution_options(autocommit=True), payload)

def get_parameters(parameters: list):
    """
    Get request parameters
    """

    args = {}

    for parameter in parameters:
        value = request.args.get(parameter[0])
        if value == '0' or value == 'false':
            value = False
        args[parameter[0]] = parameter[1](value) if value != None else parameter[2]

    return args

def send_response(output: str, cache_time: int = 0) -> Response:
    """
    Send a response
    """

    # Create response in JSON format
    resp = Response(output, mimetype='application/json')

    # Set cache header
    if cache_time == 0:
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        resp.headers['Pragma'] = 'no-cache'
    else:
        resp.headers['Cache-Control'] = f'public, must-revalidate, max-age={cache_time}'

    # Return
    return resp
