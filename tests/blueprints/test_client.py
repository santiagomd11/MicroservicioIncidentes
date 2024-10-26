import unittest
import json
from flask import Flask
from src.main import create_app
from src.models.client import db, Client, Plan, Rol

class TestClientEndpoints(unittest.TestCase):

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

    def test_create_client_success(self):
        response = self.client.post('/clients/create_client', data=json.dumps(self.client_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_create_client_missing_fields(self):
        incomplete_data = self.client_data.copy()
        del incomplete_data['name']
        response = self.client.post('/clients/create_client', data=json.dumps(incomplete_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Name and email are required', response.get_json()['error'])

    def test_create_client_invalid_email(self):
        invalid_email_data = self.client_data.copy()
        invalid_email_data['email'] = 'invalid-email'
        response = self.client.post('/clients/create_client', data=json.dumps(invalid_email_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid email format', response.get_json()['error'])

    # def test_update_client_plan_success(self):
    #     # First, create a client
    #     self.client.post('/create_client', data=json.dumps(self.client_data), content_type='application/json')
    #     update_data = {
    #         'email': 'testclient@example.com',
    #         'plan': Plan.EMPRENDEDOR.name
    #     }
    #     response = self.client.put('/update_client_plan', data=json.dumps(update_data), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Client plan updated successfully', response.get_json()['message'])

    def test_update_client_plan_not_found(self):
        update_data = {
            'idNumber': 'nonexistent',
            'plan': Plan.EMPRENDEDOR.name
        }
        response = self.client.put('/clients/update_client_plan', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Client not found', response.get_json()['error'])
    
    def test_get_client_not_found(self):
        response = self.client.get('/clients/get_client/nonexistent_id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Client with id nonexistent_id not found', response.get_json()['error'])

    def test_ping(self):
        response = self.client.get('/clients/ping')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()