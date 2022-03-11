"""
This module provides our To-Do app with database functionality.
"""
# /todo/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from todo import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

# Defining the Defualt Database Path
DEFAULT_DB_PATH = Path.home().joinpath(
    '.' + Path(__file__).stem + '_todo.json'
)


# Create a Data container to store and retrieve data from To-Do DB
class DBResponse(NamedTuple):

    todo_list   : List[Dict[str, Any]]
    error       : int


# Create a Database Handler object to read and write data to our To-Do DB
class DBHandler:

    # Initialize
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    # Read the To-Do's from DB
    def read_Todos(self) -> DBResponse:

        try:
            with self._db_path.open('r') as db_file:
                try:
                    return DBResponse(json.load(db_file), SUCCESS)

                # If the file is empty or has wrong json format, return an empty list
                except json.JSONDecodeError:
                    return DBResponse([], JSON_ERROR)

        # If file faces some IO problems
        except OSError:
            return DBResponse([], DB_READ_ERROR)

    # Write the To-Do's to DB
    def write_Todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse:

        try:
            with self._db_path.open('w') as db_file:
                json.dump(todo_list, db_file)

            return DBResponse(todo_list, SUCCESS)

        # If file faces some IO problems
        except OSError:
            return DBResponse(todo_list, DB_WRITE_ERROR)


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
