import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.main import create_app
from src.models.client import db, Client, Plan, Rol
from src.blueprints.services import clear_database
import json

class TestClearDatabaseEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing', local=True)
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        self.client_data = {
            'id': 'ed140dbe-06d8-45dc-b5fc-4eb46606fc47',
            'name': 'Test Client',
            'email': 'testclient@example.com',
            'idNumber': '123456789',
            'phoneNumber': '1234567890',
            'plan': Plan.EMPRESARIO.name,
            'rol': Rol.CLIENTE.name,
            'company': 'Test Company'
        }

    def test_clear_database_success(self):
        # create a client
        response = self.client.post('/clients/create_client', data=json.dumps(self.client_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        response = self.client.post('/clients/clear_database')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Database cleared successfully'})


if __name__ == '__main__':
    unittest.main()