import unittest
from unittest.mock import patch, MagicMock
from src.commands.search_incident_public import SearchIncidentPublic
from src.errors.errors import NotFound, ApiError
from faker import Faker
import random

class TestSearchIncidentPublicCommand(unittest.TestCase):
    def setUp(self):
        self.data_factory = Faker()
        self.user_id = self.data_factory.uuid4()
        self.incident_id = self.data_factory.uuid4()
        json_data = {
            "userId":self.user_id,
            "incidentId":self.incident_id
        }
        self.command = SearchIncidentPublic(json_data)

    @patch('src.commands.search_incident_public.Incident')
    def test_search_incident_public_success(self, mock_incident):
        date = self.data_factory.date_time()
        description = self.data_factory.paragraph(nb_sentences=1)
        solved = random.choice([True, False])

        mock_incident_instance = MagicMock()
        mock_incident_instance.id = self.incident_id
        mock_incident_instance.description = description
        mock_incident_instance.date = date
        mock_incident_instance.solved = solved

        mock_incident.query.filter_by.return_value.first.return_value = mock_incident_instance

        response = self.command.execute()

        self.assertEqual(response, {
            'id': self.incident_id,
            'description': description,
            'date': date,
            'solved': solved
        })

    @patch('src.commands.search_incident_public.Incident')
    def test_search_incident_public_not_found(self, mock_incient):
        mock_incient.query.filter_by.return_value.first.return_value = None

        with self.assertRaises(NotFound) as context:
            self.command.execute()

        self.assertEqual(str(context.exception), f'El incidente no fue encontrado')

    @patch('src.commands.search_incident_public.db')
    @patch('src.commands.search_incident_public.Incident')
    def test_search_incident_public_api_error(self, mock_incident, mock_db):
        mock_incident.query.filter_by.side_effect = Exception('DB Error')

        with self.assertRaises(ApiError):
            self.command.execute()

        mock_db.session.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()