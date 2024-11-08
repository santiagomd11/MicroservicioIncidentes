import unittest
from unittest.mock import patch
from src.main import create_app
from src.commands.clear_database import ClearDatabase
from src.errors.errors import ApiError

class TestClearDatabaseCommand(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing', local=True)
        self.client = self.app.test_client()

    @patch('src.commands.clear_database.db')
    def test_clear_database_success(self, mock_db):
        command = ClearDatabase()
        command.execute()
        mock_db.session.commit.assert_called_once()
        mock_db.session.rollback.assert_not_called()

if __name__ == '__main__':
    unittest.main()
