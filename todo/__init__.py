"""
Top level package of our To-Do App
"""
# todo/__init__.py

__app_name__    = 'todo'
__version__     = '0.1.0'

# Defining the List of Key Words
(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

# Defining Errors
ERRORS = {
    DIR_ERROR       :   'Config directory error',
    FILE_ERROR      :   'Config file error',
    DB_READ_ERROR   :   'Database read error',
    DB_WRITE_ERROR  :   'Database write error',
    JSON_ERROR      :   'To-Do ID error'
}
