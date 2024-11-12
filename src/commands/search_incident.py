from src.commands.base_command import BaseCommand
from src.models.incident import Incident, db
from src.errors.errors import NotFound, BadRequest, ApiError

class SearchIncident(BaseCommand):
    def __init__(self, json):
        self.user_id = json.get('userId', '').strip()
        self.incident_id = json.get('incidentId', '').strip()
        self.company = json.get('company') if json.get('company') is not None else ''
        self.company.strip()

    def execute(self):
        incident = ""
        try:
            if self.company != '':
                incident = Incident.query.filter_by(id=self.incident_id, user_id=self.user_id, company=self.company).first()
            else:
                incident = Incident.query.filter_by(id=self.incident_id, user_id=self.user_id).first()
        except Exception as e:
            db.session.rollback()
            raise ApiError()

        if not incident:
            raise NotFound("El incidente no fue encontrado")

        incident_info = {
            'id': incident.id,
            'type': incident.type.name,
            'description': incident.description,
            'date': incident.date,
            'userId': incident.user_id,
            'channel': incident.channel.name,
            'agentId': incident.agent_id,
            'company': incident.company,
            'solved': incident.solved,
            'response': incident.response
        }

        return incident_info

        
