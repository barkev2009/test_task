import requests


def test_post_limit():
    response = requests.post('http://127.0.0.1:8000/api/limits?id=4&cur=usd&country=rus&max_limit=4000')
    assert response.json()['status'] == 'success' and response.json()['result']['ID'] == 4 and \
           response.json()['result']['COUNTRY'] == 'RUS' and response.json()['result']['CUR'] == 'USD' and \
           response.json()['result']['MAX_LIMIT'] == 4000


def test_put_limit_cur_max_limit():
    response = requests.put('http://127.0.0.1:8000/api/limits?id=4&cur=rub&max_limit=1000')
    assert response.json()['status'] == 'success' and response.json()['result']['ID'] == 4 and \
           response.json()['result']['CUR'] == 'RUB' and response.json()['result']['MAX_LIMIT'] == 1000


def test_put_limit_incorrect():
    response = requests.put('http://127.0.0.1:8000/api/limits?id=4&cur=r&max_limit=1000')
    assert response.json()['status'] == 'failure'


def test_delete_limit():
    response = requests.delete('http://127.0.0.1:8000/api/limits/4')
    assert response.json()['status'] == 'success' and response.json()['message'] == 'limit of id=4 deleted'


def test_delete_limit_incorrect():
    response = requests.delete('http://127.0.0.1:8000/api/limits/444')
    assert response.json()['status'] == 'failure'


def test_post_incorrect_limit():
    response = requests.post('http://127.0.0.1:8000/api/limits?id=4&cur=us&country=rus&max_limit=4000')
    assert response.json()['status'] == 'failure'


def test_post_history_now():
    response = requests.post('http://127.0.0.1:8000/api/history?id=2&cur=usd&country=rus&amount=1&date=now')
    assert response.json()['status'] == 'success'


def test_post_history_date_12():
    response = requests.post('http://127.0.0.1:8000/api/history?id=2&cur=usd&country=rus&amount=1&date=2021-12-12T12:12:12')
    assert response.json()['status'] == 'success'


def test_post_history_incorrect_sum():
    response = requests.post('http://127.0.0.1:8000/api/history?id=1&cur=usd&country=rus&amount=99999&date=now')
    assert response.json()['status'] == 'failure'


def test_post_history_incorrect_id():
    response = requests.post('http://127.0.0.1:8000/api/history?id=444&cur=usd&country=rus&amount=9&date=now')
    assert response.json()['status'] == 'failure'


def test_post_history_incorrect_cur():
    response = requests.post('http://127.0.0.1:8000/api/history?id=1&cur=usd&country=ru&amount=9&date=now')
    assert response.json()['status'] == 'failure'


def test_get_all_limits():
    response = requests.get('http://127.0.0.1:8000/api/limits')
    assert response.json()['status'] == 'success'


def test_get_limits_by_id_status():
    response = requests.get('http://127.0.0.1:8000/api/limits/1')
    assert response.json()['status'] == 'success'


def test_get_limits_by_id_correct_id():
    response = requests.get('http://127.0.0.1:8000/api/limits/1')
    assert response.json()['data']['ID'] == 1


def test_get_limits_by_id_incorrect():
    response = requests.get('http://127.0.0.1:8000/api/limits/444')
    assert response.json()['status'] == 'failure'
