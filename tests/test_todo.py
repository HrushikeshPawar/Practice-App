"""
Unit testing code.
"""
# test/test_todo.py

from typer.testing import CliRunner
from todo import __app_name__, __version__, cli


# Initialize the CLI Runner(Typer Application)
runner = CliRunner()


# Test the version command
def test_version():
    result = runner.invoke(cli.app, ['--version'])
    assert result.exit_code == 0
    assert f'{__app_name__} v{__version__}\n' in result.stdout

    result = runner.invoke(cli.app, ['-v'])
    assert result.exit_code == 0
    assert f'{__app_name__} v{__version__}\n' in result.stdout
