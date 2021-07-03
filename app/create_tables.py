import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.table_handler import insert_into_limits
from app import DATABASE_NAME
from utils import PostgreSQLStarter


def create_db():
    """
    Create PostgreSQL database with name from app/__init__.py
    :return:
    """
    connection, cursor = PostgreSQLStarter(database_exists=False).get_connection_and_cursor()
    sql_create_database = 'create database {}'
    cursor.execute(sql_create_database.format(DATABASE_NAME))
    cursor.close()
    connection.close()


def create_tables():
    """
    Create limits and history table in PostgreSQL database
    and insert first 3 rows into limits table for proper testing
    :return:
    """
    connection, cursor = PostgreSQLStarter().get_connection_and_cursor()
    create_limits_query = '''CREATE TABLE limits
        (ID INT PRIMARY KEY     NOT NULL,
        COUNTRY TEXT    NOT NULL,
        CUR TEXT    NOT NULL,
        MAX_LIMIT REAL);'''
    create_history_query = '''CREATE TABLE history
        (ID INT     NOT NULL,
        DATE TIMESTAMP  NOT NULL,
        AMOUNT REAL,
        CUR TEXT    NOT NULL,
        COUNTRY TEXT    NOT NULL);
        '''
    for query in [create_limits_query, create_history_query]:
        cursor.execute(query)
        connection.commit()
        print('Table successfully created')
    insert_into_limits(1, 'RUS', 'RUB', 5000, connection, cursor)
    insert_into_limits(2, 'AUS', 'USD', 5000, connection, cursor)
    insert_into_limits(3, 'ABH', 'EUR', 5000, connection, cursor)
    cursor.close()
    connection.close()


if __name__ == '__main__':
    create_db()
    create_tables()
