from fastapi.testclient import TestClient
from app import main

def test_reservations_and_conflicts(tmp_path, monkeypatch):
    monkeypatch.setattr(main, 'DB', 'sqlite:///' + str(tmp_path / 'test.db'))
    with TestClient(main.app) as client:
        assert client.get('/health').json() == {'status': 'ok'}
        body = {'resource': 'tokyo-room', 'customer': '山田', 'starts_at': '2027-01-01T10:00:00+09:00'}
        first = client.post('/reservations', json=body)
        assert first.status_code == 201
        assert client.get('/reservations/' + first.json()['id']).json() == first.json()
        body['starts_at'] = '2027-01-01T01:00:00Z'
        assert client.post('/reservations', json=body).status_code == 409
        body['starts_at'] = '2027-01-01T10:00:00'
        assert client.post('/reservations', json=body).status_code == 422
        assert client.get('/reservations/not-found').status_code == 404

def test_parallel_requests_only_book_once(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    monkeypatch.setattr(main, 'DB', 'sqlite:///' + str(tmp_path / 'concurrency.db'))
    with TestClient(main.app) as client:
        body = {'resource': 'room', 'customer': 'demo', 'starts_at': '2027-02-01T12:00:00+09:00'}
        with ThreadPoolExecutor(max_workers=8) as pool:
            codes = list(pool.map(lambda _: client.post('/reservations', json=body).status_code, range(8)))
        assert codes.count(201) == 1
        assert codes.count(409) == 7

def test_demo_and_invalid_input(tmp_path, monkeypatch):
    monkeypatch.setattr(main, 'DB', 'sqlite:///' + str(tmp_path / 'demo.db'))
    with TestClient(main.app) as client:
        assert '予約を作成' in client.get('/').text
        assert client.post('/reservations', json={'resource': '  ', 'customer': 'test', 'starts_at': '2027-01-01T10:00:00+09:00'}).status_code == 422
        assert client.post('/reservations', json={'resource': 'room', 'customer': 'test', 'starts_at': 'invalid'}).status_code == 422
