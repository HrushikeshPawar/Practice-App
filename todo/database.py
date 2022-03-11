"""
This module provides our To-Do app with database functionality.
"""
# todo/database.py

import configparser
from pathlib import Path
from todo import DB_WRITE_ERROR, SUCCESS

# Defining the Defualt Database Path
DEFAULT_DB_PATH = Path.home().joinpath(
    '.' + Path(__file__).stem + '_todo.json'
)


# Returns the current path to the Database
def get_database_path(cofig_file: Path) -> Path:

    config_parser = configparser.ConfigParser()
    config_parser.read(cofig_file)
    return Path(config_parser['General']['database'])


# Create out To-Do database
def init_database(db_path: Path) -> int:

    try:
        # Start with empty To-Do list
        db_path.write_text('[]')
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
