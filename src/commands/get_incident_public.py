from src.commands.base_command import BaseCommand
from src.errors.errors import NotFound, ApiError
from src.models.incident import Incident, db

class GetIncidentPublic(BaseCommand):
    def __init__(self, incident_id):
        self.incident_id = incident_id

    def execute(self):
        incident = ""
        try:
            incident = Incident.query.filter_by(id=self.incident_id).first()
        except Exception as e:
            db.session.rollback()
            raise ApiError() from e
        
        if not incident:
            raise NotFound(f'Incidente no encontrado')

        incident_info = {
            'id': incident.id,
            'type': incident.type.name,
            'description': incident.description,
            'date': incident.date,
            'solved': incident.solved,
            'response': incident.response
        }

        return incident_info