import sqlite3
from constants import CsvCols


def connect_db(path):
    """
    Creates a connection the DB at the given path.
    If a DB at the given path does not exist, a new
    DB will be created.
    :param str path: path to database
    :returns: a connection and cursor pointing to the database at the given path
    :rtype: sqlite3.Connection, sqlite3.Cursor
    """
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    query = cursor.execute("SELECT name FROM sqlite_master")
    result = query.fetchone()
    if result is not None and 'expenses' in result:
        return connection, cursor

    cursor.execute("CREATE TABLE expenses("
                   "vendor TEXT NOT NULL PRIMARY KEY, "
                   "category TEXT NOT NULL)")

    return connection, cursor


def get_vendors_to_add(df, cursor):
    """
    Returns the names of the vendors in the given dataframe
    that do not exist in the database.
    :param pandas.DataFrame df: expense dataframe
    :param sqlite3.Cursor cursor: cursor to expense database
    :return: the list of vendors that need to be added to the database
    :rtype: List[str]
    """
    vendors_in_csv = set(df[CsvCols.VENDOR])
    query_str = 'SELECT vendor FROM expenses'
    result = cursor.execute(query_str).fetchall()
    vendors_in_db = set(*zip(*result))
    vendors_to_add = vendors_in_csv - vendors_in_db
    return sorted(vendors_to_add)


def add_vendors_to_db(connection, cursor, categorized_vendors):
    cursor.executemany('INSERT INTO expenses VALUES(?, ?)', categorized_vendors)
    connection.commit()


def map_vendors_to_categories(cursor, vendors):
    vendors_to_categories = dict()
    for vendor in vendors:
        category = cursor.execute('SELECT category FROM expenses WHERE vendor == ?', (vendor,)).fetchone()
        if len(category) != 1:
            continue
        vendors_to_categories[vendor] = category[0]

    return vendors_to_categories
