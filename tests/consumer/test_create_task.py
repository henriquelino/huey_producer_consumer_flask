import json
from loguru import logger  # noqa: F401
from src.app.consumer.main import app



class TestEndpoints:
    @classmethod
    def setup_class(cls):
        # create a test client for the Flask app
        cls.client = app.test_client()

    def test_start_endpoint(self):
        # send a GET request to the /start endpoint
        response = self.client.get('/start')

        # assert that the response code is 200 OK
        assert response.status_code == 200

        # assert that the response data is a JSON object containing a state field with value "running"
        assert json.loads(response.data)['state'] == 'running'

    def test_stop_endpoint(self):
        # send a GET request to the /stop endpoint
        response = self.client.get('/stop')

        # assert that the response code is 200 OK
        assert response.status_code == 200

        # assert that the response data is a JSON object containing a state field with value "stopped"
        assert json.loads(response.data)['state'] == 'stopped'

    def test_status_endpoint(self):
        # send a GET request to the /status endpoint
        response = self.client.get('/status')

        # assert that the response code is 200 OK
        assert response.status_code == 200

        # assert that the response data is a JSON object containing a status field with value "running"
        status_data = {'state': 'stopped'}
        assert json.loads(response.data) == status_data

    @classmethod
    def teardown_class(cls):
        # clean up after the tests have finished running
        pass
    
    