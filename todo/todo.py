"""
This module provides our To-Do app with Model controller.
This is the heart of our To-Do app.
"""
# todo/models.py

from pathlib import Path
from typing import Any, Dict, NamedTuple

from database import DBHandler


# Object to store the data received from CLI
class CurrentTodo(NamedTuple):

    # The class has two fields with following properties
    # This is to store the data received from the CLI
    todo    : Dict[str, Any]
    error   : int


# Setting up the exchange mechanism between CLI and DB
class Todoer:

    # Initialize
    def __init__(self, db_path: Path) -> None:
        self._db_handle = DBHandler(db_path)
