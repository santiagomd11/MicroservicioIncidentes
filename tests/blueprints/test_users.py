import unittest
from flask import Flask
from src.main import create_app, logger
from src.models import db

class TestUserEndpoints(unittest.TestCase):
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
    
    def create_user(self):
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
        return user_response, user_payload["company"]

    def test_create_user(self):
        user_response, _ = self.create_user()
        self.assertEqual(user_response.status_code, 201)
        self.assertIn('id', user_response.get_json())
        self.assertIsInstance(user_response.get_json()['id'], str)

    def test_get_user(self):
        user_response, company = self.create_user()
        user_id = user_response.get_json()['id']
        response = self.client.get(f'/incidents/get_user/{user_id}/{company}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), dict)
        self.assertEqual(response.get_json()['id'], user_id)

if __name__ == '__main__':
    unittest.main()