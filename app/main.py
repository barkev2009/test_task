from aiohttp import web
import json
from app.table_handler import *
from datetime import datetime
from app import POSTGRESQL_HOST
from utils import PostgreSQLStarter


async def get_all_limits_handler(request):
    """
    Handler for method 'GET', entire limits table
    :param request:
    :return:
    """
    try:
        table = get_limits_table(cursor)
        request_obj = {'status': 'success', 'data': table}
        return web.Response(text=json.dumps(request_obj, indent=4), status=200)
    except Exception as e:
        request_obj = {'status': 'failure', 'message': str(e)}
        return web.Response(text=json.dumps(request_obj, indent=4), status=500)


async def get_limit_by_id_handler(request):
    """
    Handler for method 'GET', row with a certain ID of the limits table
    :param request:
    :return:
    """
    try:
        id = int(str(request.url).split('/')[-1])
        response = get_limit_by_id(id, cursor)
        if response.get('failure') is None:
            request_obj = {'status': 'success', 'data': response}
            return web.Response(text=json.dumps(request_obj, indent=4), status=200)
        else:
            request_obj = {'status': 'failure', 'message': f'ID={id} does not exist'}
            return web.Response(text=json.dumps(request_obj, indent=4), status=418)
    except Exception as e:
        request_obj = {'status': 'failure', 'message': str(e)}
        return web.Response(text=json.dumps(request_obj, indent=4), status=500)


async def post_limits_handler(request):
    """
    Handler for method 'POST', new limit record
    :param request:
    :return:
    """
    try:
        id, country, currency, max_limit = request.query['id'], request.query['country'], request.query['cur'], \
                                           request.query['max_limit']
        print(f'Creating a new record in limits table')
        result = insert_into_limits(int(id), country.upper(), currency.upper(), float(max_limit), connection, cursor)
        if result.get('failure') is None:
            request_obj = {'status': 'success', 'message': 'limits updated', 'result': result}
            return web.Response(text=json.dumps(request_obj, indent=4), status=200)
        else:
            request_obj = {'status': 'failure', 'message': 'limits not updated', 'result': result}
            return web.Response(text=json.dumps(request_obj, indent=4), status=418)
    except Exception as e:
        request_obj = {'status': 'failure', 'message': str(e)}
        return web.Response(text=json.dumps(request_obj, indent=4), status=500)


async def post_history_handler(request):
    """
    Handler for method 'POST', new history record
    :param request:
    :return:
    """
    try:
        id, date, amount, currency, country = request.query['id'], request.query['date'], request.query['amount'], \
                                           request.query['cur'], request.query['country']
        print(f'Creating a new record in history table')
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if date == 'now' else date.replace('T', ' ')
        result = insert_into_history(int(id), date_time, float(amount), currency.upper(), country.upper(),
                                     connection, cursor)
        if result.get('failure') is None:
            request_obj = {'status': 'success', 'message': 'history updated', 'result': result}
            return web.Response(text=json.dumps(request_obj, indent=4), status=200)
        else:
            if 'exceeds' in result.get('failure'):
                status_code = 400
            else:
                status_code = 418
            request_obj = {'status': 'failure', 'message': 'history not updated', 'result': result}
            return web.Response(text=json.dumps(request_obj, indent=4), status=status_code)
    except Exception as e:
        request_obj = {'status': 'failure', 'message': str(e)}
        return web.Response(text=json.dumps(request_obj, indent=4), status=500)


async def put_limits_handler(request):
    """
    Handler for method 'PUT', update row with a certain ID of the limits table
    :param request:
    :return:
    """
    try:
        id = int(request.query['id'])
        country = request.query['country'].upper() if 'country' in request.query.keys() else None
        currency = request.query['cur'].upper() if 'cur' in request.query.keys() else None
        max_limit = float(request.query['max_limit']) if 'max_limit' in request.query.keys() else None
        print(f'Updating limits table')
        result = update_limits(id, connection, cursor, currency, country, max_limit)
        if result is None:
            request_obj = {'status': 'failure', 'message': 'limits not updated', 'result': 'check inputs'}
            return web.Response(text=json.dumps(request_obj, indent=4), status=418)
        else:
            request_obj = {'status': 'success', 'message': 'limits updated', 'result': result}
            return web.Response(text=json.dumps(request_obj, indent=4), status=200)
    except Exception as e:
        request_obj = {'status': 'failure', 'message': str(e)}
        print(e)
        return web.Response(text=json.dumps(request_obj, indent=4), status=500)


async def delete_limit_handler(request):
    """
    Handler for method 'DELETE', remove a row with a certain ID from the limits table
    :param request:
    :return:
    """
    try:
        id = int(str(request.url).split('/')[-1])
        result = delete_from_limits_by_id(id, connection, cursor)
        if result.get('failure') is None:
            request_obj = {'status': 'success', 'message': f'limit of id={id} deleted'}
            return web.Response(text=json.dumps(request_obj, indent=4), status=200)
        else:
            request_obj = {'status': 'failure', 'message': f'limit of id={id} does not exist'}
            return web.Response(text=json.dumps(request_obj, indent=4), status=418)
    except Exception as e:
        request_obj = {'status': 'failure', 'message': str(e)}
        return web.Response(text=json.dumps(request_obj, indent=4), status=500)


if __name__ == '__main__':
    connection, cursor = PostgreSQLStarter().get_connection_and_cursor()
    app = web.Application()
    app.add_routes([
        web.get('/api/limits', get_all_limits_handler),
        web.get('/api/limits/{id}', get_limit_by_id_handler),
        web.post('/api/limits', post_limits_handler),
        web.post('/api/history', post_history_handler),
        web.put('/api/limits', put_limits_handler),
        web.delete('/api/limits/{id}', delete_limit_handler),
    ])

    web.run_app(app, port=8000, host=POSTGRESQL_HOST)
