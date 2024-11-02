import unittest
from flask import Flask
from src.main import create_app

class TestClearDatabaseEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing', local=True)
        self.client = self.app.test_client()

    def test_clear_database(self):
        response = self.client.post('/incidents/clear_database')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Database cleared successfully'})

if __name__ == '__main__':
    unittest.main()