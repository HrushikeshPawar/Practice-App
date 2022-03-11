"""
Unit testing code.
"""
# test/test_todo.py

import json
import pytest
from typer.testing import CliRunner
from todo import __app_name__, __version__, cli, SUCCESS, todo


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


# Test the init command
def test_init():
    result = runner.invoke(cli.app, ['init'])
    assert result.exit_code == 0
    assert 'To-Do database location? ' in result.stdout


# Test Todoer.add() function
# First create a Tmp DB for performing the test
@pytest.fixture
def mock_json_file(tmp_path):
    task = [{"Description": "Get some milk.", "Priority": 2, "Done": False}]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(task, db)
    return db_file


# Once we have a Tmp DB, we create some test data
# First two keys represent the input data while the third key represents the expected return value
test_data1 = {
    "description": ["Clean", "the", "house"],
    "priority": 1,
    "todo": {
        "Description": "Clean the house.",
        "Priority": 1,
        "Done": False,
    },
}
test_data2 = {
    "description": ["Wash the car"],
    "priority": 2,
    "todo": {
        "Description": "Wash the car.",
        "Priority": 2,
        "Done": False,
    },
}


# We use the parametrization from pytest to provide multiple arguments and expected results
@pytest.mark.parametrize(
    'description, priority, expected',
    [
        pytest.param(
            test_data1["description"],
            test_data1["priority"],
            (test_data1["todo"], SUCCESS),
        ),
        pytest.param(
            test_data2["description"],
            test_data2["priority"],
            (test_data2["todo"], SUCCESS),
        ),
    ],
)
# Test the add function
def test_add(mock_json_file, description, priority, expected):

    # Initialize the Todoer object
    todoer = todo.Todoer(mock_json_file)

    assert todoer.add(description, priority) == expected
    read = todoer._db_handler.read_Todos()
    assert len(read.todo_list) == 2
