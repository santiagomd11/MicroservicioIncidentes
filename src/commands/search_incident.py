from src.commands.base_command import BaseCommand
from src.models.incident import Incident, db
from src.errors.errors import NotFound, BadRequest, ApiError

class SearchIncident(BaseCommand):
    def __init__(self, json):
        self.user_id = json.get('userId', '').strip()
        self.incident_id = json.get('incidentId', '').strip()

    def execute(self):
        try:
            query = Incident.query

            if self.incident_id and self.user_id:
                query = query.filter_by(user_id=self.user_id, id=self.incident_id)
            else:
                raise BadRequest('Both user_id and incidentId are required in the search criteria')

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
                    'channel': incident.channel.name
                }
                for incident in incidents
            ]

            return incidents_info

        except Exception as e:
            db.session.rollback()
            raise ApiError()
