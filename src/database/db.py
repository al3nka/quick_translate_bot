"""
File contains methods for working with database
"""
import sqlite3

sqlite_connection = sqlite3.connect('database/users.db')
cursor = sqlite_connection.cursor()


def insert(table: str, column_values: dict):
    """
    Method to insert data to table of database
    :param table: name of database table
    :param column_values: dictionary of column-value pairs to insert in database
    """
    columns = ", ".join(column_values.keys())
    values = tuple(column_values.values())
    cursor.execute(
        f"INSERT INTO {table}"
        f"({columns}) "
        f"VALUES {values}"
    )
    sqlite_connection.commit()


def delete(table: str, row_id: int):
    """
    Method to delete row from database table
    :param table: table name
    :param row_id: id of the row to delete
    """
    cursor.execute(
        f"DELETE FROM {table}"
        f"WHERE telegram_id={row_id};"
    )
    sqlite_connection.commit()


def update(table: str, row_id: int, column_values: dict):
    """
    Method to update values in database
    :param table: table name
    :param row_id: id of row
    :param column_values: dictionary of column-value pairs to change in database
    """
    new_values = (tuple(zip(column_values.keys(),
                            column_values.values())
                        )
                  )
    for column, value in new_values:
        cursor.execute(
            f"UPDATE {table} "
            f"SET {column} = '{value}' "
            f"WHERE telegram_id = {row_id};"
        )
    sqlite_connection.commit()


def get_col(table: str, user_id, col_name: str) -> str:
    """
    Method to get value from database
    :param table: table name
    :param user_id: id of row
    :param col_name: name of column to get value
    """
    cursor.execute(
        f"SELECT {col_name} "
        f"FROM {table} "
        f"WHERE telegram_id={user_id}"
    )
    result = cursor.fetchone()
    if result:
        result = " ".join(map(str, result))
    return result


def _init_db():
    """
    Method to create database
    """
    with open("database/createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    sqlite_connection.commit()


def check_db_exists():
    """
    This method checks if database exists and if not, creates it
    """
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
