import unittest
from unittest.mock import patch
from src.commands.get_incident_public import GetIncidentPublic
from src.errors.errors import NotFound, ApiError
from faker import Faker

class TestGetIncidentPublicCommand(unittest.TestCase):
    def setUp(self):
        self.data_factory = Faker()
        self.user_id = self.data_factory.uuid4()
        self.incident_id = self.data_factory.uuid4()

        self.command = GetIncidentPublic(self.incident_id)


    @patch('src.commands.get_incident_public.Incident')
    def test_get_incident_public_not_found(self, mock_incient):
        mock_incient.query.filter_by.return_value.first.return_value = None

        with self.assertRaises(NotFound) as context:
            self.command.execute()

        self.assertEqual(str(context.exception), f'Incidente no encontrado')

    @patch('src.commands.get_incident_public.db')
    @patch('src.commands.get_incident_public.Incident')
    def test_get_incident_public_api_error(self, mock_incident, mock_db):
        mock_incident.query.filter_by.side_effect = Exception('DB Error')

        with self.assertRaises(ApiError):
            self.command.execute()

        mock_db.session.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()