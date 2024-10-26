import unittest
from flask import Flask
from src.main import create_app

class TestPingEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing', local=True)
        self.client = self.app.test_client()

    def test_ping(self):
        response = self.client.get('/clients/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'pong'})

if __name__ == '__main__':
    unittest.main()