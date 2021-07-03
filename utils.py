import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app import POSTGRESQL_USER, POSTGRESQL_PASSWORD, POSTGRESQL_HOST, POSTGRESQL_PORT, DATABASE_NAME, ALLOW_PARSING
from bs4 import BeautifulSoup
import requests


class PostgreSQLStarter:
    """
    Class to start and return connection and cursor instances from psycopg2
    depending on the existence of the database
    """
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


def exchange_into_rub(money_data, exchange_rates):
    rubbles = euros = dollars = 0
    for item in money_data:
        if item[1] == 'RUB':
            rubbles += item[0]
        elif item[1] == 'USD':
            dollars += item[0]
        elif item[1] == 'EUR':
            euros += item[0]
    return rubbles + exchange_rates['USD'] * dollars + exchange_rates['EUR'] * euros


def get_exchange_rates(allow_parsing=ALLOW_PARSING):
    """
    Either parse exchange rates from cbr.ru or set constant rates
    :param allow_parsing:
    :return:
    """
    if allow_parsing:
        try:
            html = requests.get('https://cbr.ru/currency_base/daily/')
            bs = BeautifulSoup(html.text, 'html.parser')

            rows = bs.select_one('table.data').find_all('tr')
            exchange_rates = {}
            for i, row in enumerate(rows):
                if i != 0:
                    currency, value = row.text.split('\n')[2], float(row.text.split('\n')[-2].replace(',', '.'))
                    if currency == 'USD' or currency == 'EUR':
                        exchange_rates[currency] = value
        except Exception:
            exchange_rates ={'USD':  70, 'EUR': 80}
    else:
        exchange_rates = {'USD': 70, 'EUR': 80}
    return exchange_rates


if __name__ == '__main__':
    print(exchange_into_rub([(200, 'RUB',), (200, 'USD',), (200, 'EUR',)],
                            get_exchange_rates()))