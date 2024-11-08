import unittest
from unittest.mock import patch, MagicMock
from src.commands.get_user import GetUser
from src.errors.errors import NotFound, ApiError
from src.models.user import User

class TestGetUserCommand(unittest.TestCase):
    def setUp(self):
        self.user_id = '123'
        self.company = 'Example Inc.'
        self.command = GetUser(self.user_id, self.company)

    @patch('src.commands.get_user.User')
    def test_get_user_success(self, mock_user):
        mock_user_instance = MagicMock()
        mock_user_instance.id = self.user_id
        mock_user_instance.name = 'John Doe'
        mock_user_instance.phone = '1234567890'
        mock_user_instance.email = 'john.doe@example.com'
        mock_user_instance.incidents = []

        mock_user.query.filter_by.return_value.first.return_value = mock_user_instance

        response = self.command.execute()

        self.assertEqual(response, {
            'id': self.user_id,
            'name': 'John Doe',
            'phone': '1234567890',
            'email': 'john.doe@example.com',
            'incidents': []
        })

    @patch('src.commands.get_user.User')
    def test_get_user_not_found(self, mock_user):
        mock_user.query.filter_by.return_value.first.return_value = None

        with self.assertRaises(NotFound) as context:
            self.command.execute()

        self.assertEqual(str(context.exception), f'User with id {self.user_id} not found')

    @patch('src.commands.get_user.db')
    @patch('src.commands.get_user.User')
    def test_get_user_api_error(self, mock_user, mock_db):
        mock_user.query.filter_by.side_effect = Exception('DB Error')

        with self.assertRaises(ApiError):
            self.command.execute()

        mock_db.session.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()