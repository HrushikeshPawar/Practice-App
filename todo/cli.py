"""
This module contains the code for our To-Do CLI.
"""
# /todo/cli.py

import typer
from pathlib import Path
from typing import Optional, List
from todo import __app_name__, __version__, ERRORS, config, database, todo

# Initialize the CLI (Typer Application)
app = typer.Typer()


# Define the init command
@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_PATH),
        '--db-path',
        '-db',
        prompt='To-Do database location? ',
    ),
) -> None:

    # Initialize the config file
    app_init_error = config.init_app(db_path)

    # If config Initialization fails, invoke correct errors and exit
    if app_init_error:
        typer.secho(
            f'Creating config file failed with {ERRORS[app_init_error]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # Initialize the database
    db_init_error = database.init_database(Path(db_path))

    # If database Initialization fails, invoke correct errors and exit
    if db_init_error:
        typer.secho(
            f'Creating database failed with {ERRORS[db_init_error]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    else:
        typer.secho(f'The To-Do database is {db_path}', fg=typer.colors.GREEN)


# Creating Todoer with valid config file and DB
def get_todoer() -> todo.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "todo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    if db_path.exists():
        return todo.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "todo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


# Define the add command for cli
@app.command()
def add(
    description: List[str] = typer.Argument(...),
    priority: int = typer.Option(2, '--priority', '-p', min=1, max=4),
) -> None:

    # Create a Todoer object
    todoer = get_todoer()

    # Add a new task
    Todo, error = todoer.add(description, priority)

    # Check for errors
    if error:
        typer.secho(f'Adding To-Do failed with {ERRORS[error]}', fg=typer.colors.RED)
        raise typer.Exit(1)

    else:
        # Print the task added
        typer.secho(
            f'To-Do: {description} was added with priority: {priority}',
            fg=typer.colors.GREEN
        )


# Define the list command for cli
@app.command(name='list')
def list_all() -> None:

    # Initialize the Todoer object
    todoer = get_todoer()

    # Get todo list from DB
    todo_list = todoer.get_Todo_list()

    # Check if there are any tasks in the list
    if len(todo_list) == 0:
        typer.secho(
            'There are no tasks in the list. Please, add some',
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit()

    # Print the list of tasks
    else:

        typer.secho('\nTo-Do List:\n', fg=typer.colors.BLUE, bold=True)

        # Columns for our table
        columns = (
            'ID.    ',
            '|  Priority   ',
            '|  Done?  ',
            '|  Description  ',
        )

        header = ''.join(columns)
        typer.secho(header, fg=typer.colors.BLUE, bold=True)
        typer.secho('-' * len(header), fg=typer.colors.BLUE)

        for id, Todo in enumerate(todo_list, 1):

            desc, priority, done = Todo.values()

            if done:
                COLOR = typer.colors.GREEN

            elif priority == 1:
                COLOR = typer.colors.RED

            else:
                COLOR = typer.colors.YELLOW

            typer.secho(
                f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
                f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
                f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
                f"| {desc}",
                fg=COLOR,
            )

        typer.secho("-" * len(header) + "\n", fg=typer.colors.BLUE)


# Define the Complete command for cli
@app.command(name='complete')
def set_done(id: int = typer.Argument(...)) -> None:

    # Initialize the Todoer
    todoer = get_todoer()

    # Set the task as done
    Todo, error = todoer.set_Done(id)

    # Check for any errors
    if error:
        typer.secho(
            f'Completing To-Do #{id} failed with {ERRORS[error]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # If no errors, print the task completed
    else:
        typer.secho(
            f'To-Do #{id} - {Todo["Description"]} was completed',
            fg=typer.colors.GREEN,
        )


# Define the delete command for cli
@app.command()
def remove(
    id: int = typer.Argument(...),
    force: bool = typer.Option(
        False,
        '--force',
        '-f',
        help='Force delete the task without confirmation',
    ),
) -> None:

    # Initialize the Todoer
    todoer = get_todoer()

    # The main remove fucntion
    def _remove():
        # Remove the task
        Todo, error = todoer.remove(id)

        # Check for any errors
        if error:
            typer.secho(
                f'Removing To-Do #{id} failed with {ERRORS[error]}',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)

        # If no errors, print the task removed
        else:
            typer.secho(
                f'To-Do #{id} : {Todo["Description"]} was removed',
                fg=typer.colors.GREEN,
            )

    # If force is True, remove the task without confirmation
    if force:
        _remove()

    else:

        # Get To-Do list
        todo_list = todoer.get_Todo_list()

        # Check if the task exists
        try:
            Todo = todo_list[id - 1]

        except IndexError:
            typer.secho(
                f'To-Do #{id} does not exist',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)

        # Ask for confirmation
        if typer.confirm(
            f'Are you sure you want to remove To-Do #{id} - {Todo["Description"]}?'
        ):
            _remove()
        else:
            typer.secho(
                'To-Do not removed. Operation Cancelled',
                fg=typer.colors.YELLOW,
            )


# Define the clear command for cli
@app.command(name='clear')
def remove_all(
    force: bool = typer.Option(
        ...,
        prompt='Are you sure you want to remove all tasks?',
        help='Force delete all tasks without confirmation',
    ),
) -> None:

    # Initialize the Todoer
    todoer = get_todoer()

    # Check if force
    if force:
        error = todoer.remove_all().error

        # If any error
        if error:
            typer.secho(
                f'Removing all To-Do failed with {ERRORS[error]}',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)

        # If no errors, print the task removed
        else:
            typer.secho(
                'All To-Do were removed',
                fg=typer.colors.GREEN,
            )

    else:
        typer.secho('Operation Cancelled', fg=typer.colors.YELLOW)


# Define the version function
def _version_callback(value: bool) -> None:

    if value:

        # Print the application name and version using echo (Typer)
        typer.echo(f'{__app_name__} v{__version__}')

        # Raises Exit exception to exit the app cleanly
        raise typer.Exit()


# Define the Typer Callback function using the callback decorator.
@app.callback()
def main(

    # Define the version flag
    # It is of type bool, meaning it can be either bool or None type
    # typer.Option is a decorator that helps to defines command line argument (options).
    # The first argument, 'None' is the defualt value of the option.
    # is_eager=True tells Typer that version commoand has precedence over all other commands.
    version: Optional[bool] = typer.Option(
        None,
        '--version',
        '-v',
        help="Display the application's version",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
