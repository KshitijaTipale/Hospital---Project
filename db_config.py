import sqlite3

def get_db_connection():
    connection = sqlite3.connect('hospital.db')
    connection.row_factory = sqlite3.Row  # Returns results as dictionary-like objects
    return connection
