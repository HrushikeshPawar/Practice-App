"""
The To-Do entry point script.
"""
# todo/__main__.py

from todo import cli, __app_name__


def main():

    # Passing a value to prog_name ensures that your users get the correct app name
    # when running the --help option on their command line.
    cli.app(prog_name=__app_name__)


if __name__ == '__main__':
    main()
