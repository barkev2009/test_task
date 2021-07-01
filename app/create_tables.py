import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_db():
    connection = psycopg2.connect(user='postgres',
                                  password='1111',
                                  host='127.0.0.1',
                                  port='5432')
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = 'create database postgres_db'
    cursor.execute(sql_create_database)
    cursor.close()
    connection.close()


def create_tables():
    connection = psycopg2.connect(user='postgres',
                                  password='1111',
                                  host='127.0.0.1',
                                  port='5432',
                                  database='postgres_db')
    cursor = connection.cursor()
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
    cursor.close()
    connection.close()


if __name__ == '__main__':
    create_db()
    create_tables()