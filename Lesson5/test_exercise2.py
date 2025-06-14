import pytest
from .exercise2 import create_app

@pytest.fixture
def sample_users():
    return {'users': [
        {'name': "Spinelli"},
        {'name': "Haraguchi"},
        {'name': "Zuculini"}
    ]}

@pytest.fixture
def test_app(sample_users):
    # Cria o app com uma função fake que retorna os dados de teste
    app = create_app(lambda: sample_users)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(test_app):
    return test_app.test_client()

def test_get_users(client, sample_users):
    response = client.get('/api/users')
    assert response.status_code == 200
    assert response.get_json() == sample_users