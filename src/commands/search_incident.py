from src.commands.base_command import BaseCommand
from src.models.incident import Incident, db
from src.errors.errors import NotFound

class SearchIncident(BaseCommand):
    def __init__(self, search_criteria):
        self.search_criteria = search_criteria

    def execute(self):
        try:
            # Check if both user_id and id are in the search criteria
            if 'user_id' in self.search_criteria and 'id' in self.search_criteria:
                query = query.filter_by(user_id=self.search_criteria['user_id'], id=self.search_criteria['id'])

            incidents = query.all()
            if not incidents:
                raise NotFound('No incidents found matching the search criteria')

            incidents_info = [
                {
                    'id': incident.id,
                    'type': incident.type.name,
                    'description': incident.description,
                    'date': incident.date,
                    'user_id': incident.user_id,
                    'chanel': incident.chanel.name
                }
                for incident in incidents
            ]

            return incidents_info

        except Exception as e:
            db.session.rollback()
            raise e