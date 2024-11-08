import unittest
from unittest.mock import patch, MagicMock
from src.commands.create_user import CreateUser
from src.errors.errors import BadRequest, PreconditionFailed
from src.models.user import User, db

class TestCreateUserCommand(unittest.TestCase):
    def setUp(self):
        self.valid_json = {
            'id': '123',
            'name': 'John Doe',
            'phone': '1234567890',
            'email': 'john.doe@example.com',
            'company': 'Example Inc.'
        }

    def test_create_user_success(self):
        command = CreateUser(self.valid_json)
        with patch.object(db.session, 'add', MagicMock()) as mock_add, \
             patch.object(db.session, 'commit', MagicMock()) as mock_commit:
            response = command.execute()
            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            self.assertEqual(response, {
                'id': '123',
                'name': 'John Doe',
                'phone': '1234567890',
                'email': 'john.doe@example.com'
            })

    def test_create_user_missing_id(self):
        invalid_json = self.valid_json.copy()
        invalid_json['id'] = ''
        command = CreateUser(invalid_json)
        with self.assertRaises(BadRequest) as context:
            command.execute()
        self.assertEqual(str(context.exception), 'Id is required')

    def test_create_user_missing_name(self):
        invalid_json = self.valid_json.copy()
        invalid_json['name'] = ''
        command = CreateUser(invalid_json)
        with self.assertRaises(BadRequest) as context:
            command.execute()
        self.assertEqual(str(context.exception), 'Name is required')

    def test_create_user_missing_phone(self):
        invalid_json = self.valid_json.copy()
        invalid_json['phone'] = ''
        command = CreateUser(invalid_json)
        with self.assertRaises(BadRequest) as context:
            command.execute()
        self.assertEqual(str(context.exception), 'Phone is required')

    def test_create_user_missing_email(self):
        invalid_json = self.valid_json.copy()
        invalid_json['email'] = ''
        command = CreateUser(invalid_json)
        with self.assertRaises(BadRequest) as context:
            command.execute()
        self.assertEqual(str(context.exception), 'Email is required')

    def test_create_user_missing_company(self):
        invalid_json = self.valid_json.copy()
        invalid_json['company'] = ''
        command = CreateUser(invalid_json)
        with self.assertRaises(BadRequest) as context:
            command.execute()
        self.assertEqual(str(context.exception), 'Company is required')

    def test_create_user_precondition_failed(self):
        command = CreateUser(self.valid_json)
        with patch.object(db.session, 'add', MagicMock()) as mock_add, \
             patch.object(db.session, 'commit', MagicMock(side_effect=Exception('DB Error'))) as mock_commit, \
             patch.object(db.session, 'rollback', MagicMock()) as mock_rollback:
            with self.assertRaises(PreconditionFailed) as context:
                command.execute()
            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            mock_rollback.assert_called_once()
            self.assertEqual(str(context.exception), 'Error creating user, verify the data or if the user already exists')

if __name__ == '__main__':
    unittest.main()