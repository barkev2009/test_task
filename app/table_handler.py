import psycopg2
from datetime import datetime
import pandas as pd
from utils import exchange_into_rub

COUNTRIES_LIST = ['RUS', 'rus', 'ABH', 'abh', 'AUS', 'aus']
CURRENCIES_LIST = ['RUB', 'rub', 'USD', 'usd', 'EUR', 'eur']


def drop_table(table_name):
    cursor.execute(f'drop table {table_name}')
    connection.commit()
    print('Table dropped')


def get_limits_table(cursor):
    cursor.execute('''SELECT * FROM limits''')
    rows = cursor.fetchall()
    return [dict(zip(['ID', 'COUNTRY', 'CUR', 'MAX_LIMIT'], row)) for row in rows]


def get_limit_by_id(id, cursor):
    cursor.execute('''SELECT * FROM limits WHERE id = {}'''.format(id))
    rows = cursor.fetchall()
    return [dict(zip(['ID', 'COUNTRY', 'CUR', 'MAX_LIMIT'], row)) for row in rows]


def get_history_table(cursor):
    cursor.execute('''SELECT * FROM history''')
    rows = cursor.fetchall()
    return [dict(zip(['ID', 'DATE', 'AMOUNT', 'CUR', 'COUNTRY'], row)) for row in rows]


def insert_into_limits(id, country: str, currency: str, max_limit, connection, cursor):
    if country in COUNTRIES_LIST and currency in CURRENCIES_LIST:
        query = '''INSERT INTO limits (ID, COUNTRY, CUR, MAX_LIMIT) VALUES ({}, '{}', '{}', {})'''
        cursor.execute(query.format(id, country.upper(), currency.upper(), max_limit))
        connection.commit()
        print(f'Line ({id}, {country.upper()}, {currency.upper()}, {max_limit}) successfully inserted')
        return get_limits_table(cursor)
    else:
        print('Failed to update limits. Please, check your input')


def insert_into_history(id, date, amount, currency: str, country: str, connection, cursor):
    if country in COUNTRIES_LIST and currency in CURRENCIES_LIST:
        time_data = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        cur_month, cur_year = time_data.month, time_data.year
        next_month = cur_month + 1 if cur_month != 12 else 1
        next_year = cur_year if cur_month != 12 else cur_year + 1

        history_query = '''SELECT amount, cur FROM history WHERE date BETWEEN date '{}-{}-1' and date '{}-{}-1' '''
        cursor.execute(history_query.format(cur_year, cur_month, next_year, next_month))
        overall_to_date = exchange_into_rub(cursor.fetchall())
        rub_amount = exchange_into_rub([(amount, currency.upper())])

        limits_query = '''SELECT max_limit, cur FROM limits WHERE id = {} '''
        cursor.execute(limits_query.format(id))
        max_limit = exchange_into_rub([cursor.fetchone()])

        if overall_to_date + rub_amount <= max_limit:
            insert_query = '''INSERT INTO history (ID, DATE, AMOUNT, CUR, COUNTRY) 
                              VALUES ({}, '{}', {}, '{}', '{}')'''
            cursor.execute(insert_query.format(id, date, amount, currency.upper(), country.upper()))
            connection.commit()
            print(f'History successfully updated')
            return get_history_table(cursor)
        else:
            print(f'Sum within a current month ({overall_to_date + rub_amount}) exceeds max_limit ({max_limit})')
    else:
        print('Failed to update limits. Please, check your input')


def update_limits(id, connection, cursor, currency=None, country=None, max_limit=None):
    columns = ['CUR', 'COUNTRY', 'MAX_LIMIT']
    if country in COUNTRIES_LIST + [None] and currency in CURRENCIES_LIST + [None]:
        for i, item in enumerate([currency, country, max_limit]):
            if item is not None:
                update_query = '''UPDATE limits SET {} = '{}' WHERE ID = {}''' if columns[i] != 'MAX_LIMIT' else \
                    '''UPDATE limits SET {} = {} WHERE ID = {}'''
                cursor.execute(update_query.format(columns[i], item, id))
                connection.commit()
                print(f'Limits updated: id = {id}, {columns[i]} = {item}')
        return get_limit_by_id(id, cursor)


def delete_from_limits_by_id(id, connection, cursor):
    delete_query = '''Delete from limits where id = {}'''
    cursor.execute(delete_query.format(id))
    connection.commit()
    print(f'Record with id={id} deleted')


def show_all_pretty_tables():
    print('Limits table')
    print(pd.DataFrame.from_records(get_limits_table(cursor)))
    print('\nHistory table')
    print(pd.DataFrame.from_records(get_history_table(cursor)))


if __name__ == '__main__':
    connection = psycopg2.connect(user='postgres',
                                  password='1111',
                                  host='127.0.0.1',
                                  port='5432',
                                  database='postgres_db')
    cursor = connection.cursor()
    show_all_pretty_tables()
