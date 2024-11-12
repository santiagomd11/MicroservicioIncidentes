from src.commands.base_command import BaseCommand
from src.models.incident import Incident, db
from src.errors.errors import NotFound, ApiError

class SearchIncidentPublic(BaseCommand):
    def __init__(self, json):
        self.user_id = json.get('userId', '').strip()
        self.incident_id = json.get('incidentId', '').strip()

    def execute(self):
        incident = ""
        try:
            incident = Incident.query.filter_by(id=self.incident_id, user_id=self.user_id).first()
        except Exception as e:
            db.session.rollback()
            raise ApiError()

        if not incident:
            raise NotFound("El incidente no fue encontrado")

        incident_info = {
            'id': incident.id,
            'description': incident.description,
            'date': incident.date,
            'solved': incident.solved,
        }

        return incident_info

        