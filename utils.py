import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app import POSTGRESQL_USER, POSTGRESQL_PASSWORD, POSTGRESQL_HOST, POSTGRESQL_PORT, DATABASE_NAME


class PostgreSQLStarter:
    def __init__(self, database_exists=True):
        self.database_exists = database_exists
        if self.database_exists:
            self.connection = psycopg2.connect(user=POSTGRESQL_USER,
                                               password=POSTGRESQL_PASSWORD,
                                               host=POSTGRESQL_HOST,
                                               port=POSTGRESQL_PORT,
                                               database=DATABASE_NAME)
            self.cursor = self.connection.cursor()
        else:
            self.connection = psycopg2.connect(user=POSTGRESQL_USER,
                                               password=POSTGRESQL_PASSWORD,
                                               host=POSTGRESQL_HOST,
                                               port=POSTGRESQL_PORT)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.connection.cursor()

    def get_connection_and_cursor(self):
        return self.connection, self.cursor


def exchange_into_rub(money_data):
    rubbles = euros = dollars = 0
    for item in money_data:
        if item[1] == 'RUB':
            rubbles += item[0]
        elif item[1] == 'USD':
            dollars += item[0]
        elif item[1] == 'EUR':
            euros += item[0]
    return rubbles + 70 * dollars + 80 * euros
