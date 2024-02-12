import json

from loguru import logger  # noqa: F401

from src.consumer.main import create_flask_app


class TestEndpoints:

    @classmethod
    def setup_class(cls):
        cls.client = create_flask_app().test_client()

    def test_start_endpoint(self):
        response = self.client.get('/start')
        assert response.status_code == 200
        assert json.loads(response.data)['state'] == 'running'

        # multiple requests sequentially should return the same response
        response = self.client.get('/start')
        assert response.status_code == 200
        assert json.loads(response.data)['state'] == 'running'

    def test_stop_endpoint(self):
        response = self.client.get('/stop')
        assert response.status_code == 200
        assert json.loads(response.data)['state'] == 'stopped'

        # multiple requests sequentially should return the same response
        response = self.client.get('/stop')
        assert response.status_code == 200
        assert json.loads(response.data)['state'] == 'stopped'

    def test_status_endpoint(self):
        # status after stopping
        self.client.get('/stop')
        response = self.client.get('/status')
        assert response.status_code == 200
        status_data = {'state': 'stopped'}
        assert json.loads(response.data) == status_data

        # status after starting
        self.client.get('/start')
        response = self.client.get('/status')
        assert response.status_code == 200
        status_data = {'state': 'running'}
        assert json.loads(response.data) == status_data
