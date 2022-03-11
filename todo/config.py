"""
This module provides our To-Do app with config functionality.
"""
# todo/config.py


import configparser
from pathlib import Path
import typer

from todo import (
    DB_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__
)


#  Variables to store the app directory and config file path
CONFIG_DIR_PATH     = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH    = CONFIG_DIR_PATH / 'config.ini'


# Check the defualt paths, create them if not present
# It also returns proper error codes if something is wrong happens, otherwise returns SUCESS
def _init_config_file() -> int:

    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR

    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR

    return SUCCESS


# Checks if any errors occurs during the database creation
# Returns proper error codes if any
def _create_database(db_path: str) -> int:

    # Initialize the Config Parser
    config_parser = configparser.ConfigParser()

    config_parser['General'] = {'database': db_path}

    try:
        with CONFIG_FILE_PATH.open('w') as config_file:
            config_parser.write(config_file)
    except OSError:
        return DB_WRITE_ERROR

    return SUCCESS


def init_app(db_path: str) -> int:

    # Initialize the Application
    # Check if config file is created properly
    # Return proper error codes in case of any errors
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code

    # Check if the database is created properly
    # Return proper error codes in case of any errors
    database_code = _create_database(db_path)
    if database_code != SUCCESS:
        return database_code

    return SUCCESS
