from src.commands.base_command import BaseCommand
from src.models.incident import Incident, db
from src.errors.errors import NotFound, BadRequest, ApiError

class SearchIncident(BaseCommand):
    def __init__(self, json):
        self.user_id = json.get('userId', '').strip()
        self.incident_id = json.get('incidentId', '').strip()
        self.company = json.get('company', '').strip()

    def execute(self):
        try:
            incident = Incident.query.filter_by(id=self.incident_id, user_id=self.user_id, company=self.company).first()
            
            if not incident:
                raise NotFound(f'Incident with id {self.incident_id} not found')

            incident_info = {
                'id': incident.id,
                'type': incident.type.name,
                'description': incident.description,
                'date': incident.date,
                'userId': incident.user_id,
                'channel': incident.channel.name,
                'agentId': incident.agent_id,
                'company': incident.company,
                'solved': incident.solved
            }

            return incident_info

        except Exception as e:
            db.session.rollback()
            raise ApiError()
