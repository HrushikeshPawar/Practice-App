"""
This module provides our To-Do app with Model controller.
This is the heart of our To-Do app.
"""
# /todo/models.py

from pathlib import Path
from typing import Any, Dict, NamedTuple, List

from todo import DB_READ_ERROR, ID_ERROR
from .database import DBHandler


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
        self._db_handler = DBHandler(db_path)

    # Function to add To-Do's to the DB
    def add(self, description: List[str], priority: int = 2) -> None:

        # Add new To-Do to the DB
        description_text = ' '.join(description)

        if not description_text.endswith('.'):
            description_text += '.'

        Todo = {
            'Description'   : description_text,
            'Priority'      : priority,
            'Done'          : False,
        }

        read = self._db_handler.read_Todos()

        if read.error == DB_READ_ERROR:
            return CurrentTodo(Todo, read.error)

        read.todo_list.append(Todo)

        write = self._db_handler.write_Todos(read.todo_list)
        return CurrentTodo(Todo, write.error)

    # Function to list To-Do's from the DB
    def get_Todo_list(self) -> List[Dict[str, Any]]:

        # Return Current Todolist
        read = self._db_handler.read_Todos()
        return read.todo_list

    # Function to set the status of To-Do's as Done
    def set_Done(self, id: int) -> CurrentTodo:

        # Get the To-Do list from the DB
        read = self._db_handler.read_Todos()

        # Check if the To-Do ID is valid
        if read.error:
            return CurrentTodo({}, read.error)

        # Get the To-Do from the DB
        try:
            Todo = read.todo_list[id - 1]

        except IndexError:
            return CurrentTodo({}, ID_ERROR)

        # Set the To-Do as Done
        Todo['Done'] = True

        # Write to the DB
        write = self._db_handler.write_Todos(read.todo_list)
        return CurrentTodo(Todo, write.error)
