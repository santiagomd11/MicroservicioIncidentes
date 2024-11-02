import unittest
from flask import Flask
from src.main import create_app, logger
from src.models import db


class TestIncidentEndpoints(unittest.TestCase):
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
        # Create user for the test
        user_payload = {
            "id": "12345",
            "name": "Test User",
            "phone": "1234567890",
            "email": "testuser@example.com"
        }
        response = self.client.post('/incidents/create_user', json=user_payload)
        self.user_id = response.get_json()['id']
        
        # Create incident for the test
        incident_payload = {
            "type": "PETICION",
            "description": "Test incident",
            "date": "2023-10-01T00:00:00Z",
            "userId": f"{self.user_id}",
            "channel": "WEB"
        }
        response = self.client.post('/incidents/create_incident', json=incident_payload)
        logger.info(f"Created incident: {response.get_json()}")
        self.incident_id = response.get_json()['id']

    def test_get_incident(self):
        response = self.client.get(f'/incidents/get_incident/{self.incident_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.get_json())
        self.assertEqual(response.get_json()['id'], self.incident_id)

    def test_get_incidents(self):
        response = self.client.get('/incidents/get_incidents')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_search_incident(self):
        payload = {
            "userId": "12345",
            "incidentId": f"{self.incident_id}"  # Replace with a valid incident ID
        }
        response = self.client.post('/incidents/search_incident', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
        self.assertGreater(len(response.get_json()), 0)

if __name__ == '__main__':
    unittest.main()