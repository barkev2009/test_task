from aiohttp import web
import json
from app.table_handler import *
from datetime import datetime


async def get_all_limits_handler(request):
    table = get_limits_table(cursor)
    request_obj = {'status': 'success', 'data': table}
    return web.Response(text=json.dumps(request_obj, indent=4), status=200)


async def get_limit_by_id_handler(request):
    try:
        id = int(str(request.url).split('/')[-1])
        response = get_limit_by_id(id, cursor)
        request_obj = {'status': 'success', 'data': response}
        return web.Response(text=json.dumps(request_obj, indent=4), status=200)
    except Exception as e:
        request_obj = {'status': 'failed', 'message': str(e)}
        return web.Response(text=json.dumps(request_obj, indent=4), status=500)


async def post_limits_handler(request):
    try:
        id, country, currency, max_limit = request.query['id'], request.query['country'], request.query['cur'], \
                                           request.query['max_limit']
        print(f'Creating a new record in limits table')
        result = insert_into_limits(int(id), country.upper(), currency.upper(), float(max_limit), connection, cursor)
        request_obj = {'status': 'success', 'message': 'limits updated'}
        return web.Response(text=json.dumps(request_obj, indent=4), status=200)
    except Exception as e:
        request_obj = {'status': 'failed', 'message': str(e)}
        return web.Response(text=json.dumps(request_obj, indent=4), status=500)


async def post_history_handler(request):
    try:
        id, date, amount, currency, country = request.query['id'], request.query['date'], request.query['amount'], \
                                           request.query['cur'], request.query['country']
        print(f'Creating a new record in history table')
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if date == 'now' else date.replace('T', ' ')
        result = insert_into_history(int(id), date_time, float(amount), currency.upper(), country.upper(),
                                     connection, cursor)
        request_obj = {'status': 'success', 'message': 'history updated'}
        return web.Response(text=json.dumps(request_obj, indent=4), status=200)
    except Exception as e:
        request_obj = {'status': 'failed', 'message': str(e)}
        return web.Response(text=json.dumps(request_obj, indent=4), status=500)


async def put_limits_handler(request):
    try:
        # id, country, currency, max_limit = request.query['id'], request.query['country'], request.query['cur'], \
        #                                    request.query['max_limit']
        id = int(request.query['id'])
        country = request.query['country'].upper() if 'country' in request.query.keys() else None
        currency = request.query['cur'].upper() if 'cur' in request.query.keys() else None
        max_limit = float(request.query['max_limit']) if 'max_limit' in request.query.keys() else None
        print(f'Updating limits table')
        result = update_limits(id, connection, cursor, currency, country, max_limit)
        request_obj = {'status': 'success', 'message': 'limits updated', 'data': result}
        return web.Response(text=json.dumps(request_obj, indent=4), status=200)
    except Exception as e:
        request_obj = {'status': 'failed', 'message': str(e)}
        print(e)
        return web.Response(text=json.dumps(request_obj, indent=4), status=500)


async def delete_limit_handler(request):
    try:
        id = int(str(request.url).split('/')[-1])
        delete_from_limits_by_id(id, connection, cursor)
        request_obj = {'status': 'success', 'message': f'limit of id={id} deleted'}
        return web.Response(text=json.dumps(request_obj, indent=4), status=200)
    except Exception as e:
        request_obj = {'status': 'failed', 'message': str(e)}
        return web.Response(text=json.dumps(request_obj, indent=4), status=500)


if __name__ == '__main__':
    connection = psycopg2.connect(user='postgres',
                                  password='1111',
                                  host='127.0.0.1',
                                  port='5432',
                                  database='postgres_db')
    # connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    app = web.Application()
    app.add_routes([
        web.get('/api/limits', get_all_limits_handler),
        web.get('/api/limits/{id}', get_limit_by_id_handler),
        web.post('/api/limits', post_limits_handler),
        web.post('/api/history', post_history_handler),
        web.put('/api/limits/', put_limits_handler),
        web.delete('/api/limits/{id}', delete_limit_handler),
    ])

    web.run_app(app)
    # http://0.0.0.0:8080/api/limit?id=4&country=aus&currency=usd&max_limit=5000
    # http://0.0.0.0:8080/api/history?id=4&date=now&amount=200&cur=rub&country=rus
    # http://0.0.0.0:8080/api/history?id=4&date=2021-06-06T12:12:12&amount=200&cur=rub&country=rus
