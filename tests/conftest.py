import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    yield app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth(client):
    class AuthActions(object):
        def login(self, username='test', password='test'):
            return client.post(
                '/auth/login',
                data={'username': username, 'password': password}
            )

        def logout(self):
            return client.get('/auth/logout')

    return AuthActions()