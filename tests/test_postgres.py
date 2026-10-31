"""Optional integration test against a disposable PostgreSQL database."""
import os
import uuid
import pytest
from fastapi.testclient import TestClient
from app import main

@pytest.mark.skipif(not os.getenv('TEST_DATABASE_URL'), reason='requires disposable PostgreSQL')
def test_postgres_duplicate_slot(monkeypatch):
    monkeypatch.setattr(main, 'DB', os.environ['TEST_DATABASE_URL'])
    body = {'resource': 'test-' + str(uuid.uuid4()), 'customer': 'demo', 'starts_at': '2027-02-01T10:00:00+09:00'}
    with TestClient(main.app) as client:
        created = client.post('/reservations', json=body)
        assert created.status_code == 201
        body['starts_at'] = '2027-02-01T01:00:00Z'
        assert client.post('/reservations', json=body).status_code == 409
        assert client.get('/reservations/' + created.json()['id']).status_code == 200
