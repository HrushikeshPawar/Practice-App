"""
This module contains the code for our To-Do CLI.
"""
# todo/cli.py

from typing import Optional
import typer
from todo import __app_name__, __version__

# Initialize the CLI (Typer Application)
app = typer.Typer()


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
