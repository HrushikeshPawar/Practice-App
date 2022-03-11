"""
This module contains the code for our To-Do CLI.
"""
# todo/cli.py

from pathlib import Path
from typing import Optional
import typer
from todo import __app_name__, __version__, ERRORS, config, database

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
