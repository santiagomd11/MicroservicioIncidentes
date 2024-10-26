import unittest
from unittest.mock import patch, MagicMock
from src.commands.create_client import CreateClient
from src.errors.errors import BadRequest
from src.models.client import Client, db, Plan, Rol

class TestCreateClient(unittest.TestCase):

    def setUp(self):
        self.valid_input = {
            'id': 'ed140dbe-06d8-45dc-b5fc-4eb46606fc47',
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'idNumber': '123456789',
            'phoneNumber': '1234567890',
            'plan': Plan.EMPRESARIO,
            'rol': Rol.CLIENTE.name,
            'company': 'Test Company'
        }

    @patch('src.commands.create_client.db.session.commit')
    @patch('src.commands.create_client.db.session.add')
    @patch('src.commands.create_client.validators.email', return_value=True)
    def test_create_client_success(self, mock_valid_email, mock_add, mock_commit):
        command = CreateClient(self.valid_input)
        command.execute()
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

    def test_create_client_missing_required_fields(self):
        invalid_input = self.valid_input.copy()
        invalid_input.pop('name')
        command = CreateClient(invalid_input)
        with self.assertRaises(BadRequest) as context:
            command.execute()
        self.assertEqual(str(context.exception), 'Name and email are required')

    @patch('src.commands.create_client.validators.email', return_value=False)
    def test_create_client_invalid_email(self, mock_valid_email):
        command = CreateClient(self.valid_input)
        with self.assertRaises(BadRequest) as context:
            command.execute()
        self.assertEqual(str(context.exception), 'Invalid email format')

    @patch('src.commands.create_client.db.session.rollback')
    @patch('src.commands.create_client.db.session.add', side_effect=Exception('DB Error'))
    def test_create_client_db_error(self, mock_add, mock_rollback):
        command = CreateClient(self.valid_input)
        with self.assertRaises(Exception) as context:
            command.execute()
        self.assertEqual(str(context.exception), 'DB Error')
        mock_rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()