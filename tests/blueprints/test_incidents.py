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
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def create_user_and_incident(self):
        # Create user for the test
        user_payload = {
            "id": "12345",
            "name": "Test User",
            "phone": "1234567890",
            "email": "testuser@example.com",
            "company": "uniandes"
        }
        user_response = self.client.post('/incidents/create_user', json=user_payload)
        self.user_id = user_response.get_json()['id']
        logger.info(f"Created user: {user_response.get_json()}")
        
        # Create incident for the test
        incident_payload = {
            "type": "PETICION",
            "channel": "WEB",
            "description": "Test incident",
            "userId": f"{self.user_id}",
            "agentId": "54321",
            "company": "uniandes",

        }
        incident_response = self.client.post('/incidents/create_incident', json=incident_payload)
        logger.info(f"Created incident: {incident_response.get_json()}")
        
        return user_response, incident_response, user_payload["company"]

    
    def test_create_incident(self):
        user_response, incident_response, company = self.create_user_and_incident()
        self.assertEqual(incident_response.status_code, 201)
        self.assertIn('id', incident_response.get_json())
        self.assertIsInstance(incident_response.get_json()['id'], str)


    def test_get_incident(self):
        user_response, incident_response, company = self.create_user_and_incident()
        incident_id = incident_response.get_json()['id']
        response = self.client.get(f'/incidents/get_incident/{incident_id}/{company}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), dict)
        self.assertEqual(response.get_json()['id'], incident_id)

    def test_get_incident_public(self):
        user_response, incident_response, company = self.create_user_and_incident()
        incident_id = incident_response.get_json()['id']
        response = self.client.get(f'/incidents/public/get_incident/{incident_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), dict)
        self.assertEqual(response.get_json()['id'], incident_id)

    def test_get_incidents(self):
        response = self.client.get('/incidents/get_incidents/uniandes')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_search_incident(self):
        user_response, incident_response, company = self.create_user_and_incident()
        payload = {
            "userId": user_response.get_json()['id'],
            "incidentId": incident_response.get_json()['id'],
            "company": company
        }
        response = self.client.post('/incidents/search_incident', json=payload)
        self.assertEqual(response.status_code, 200)

    def test_search_incident_public(self):
        user_response, incident_response, company = self.create_user_and_incident()
        payload = {
            "userId": user_response.get_json()['id'],
            "incidentId": incident_response.get_json()['id'],
        }
        response = self.client.post('incidents/public/search_incident', json=payload)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()