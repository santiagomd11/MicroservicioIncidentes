from src.commands.base_command import BaseCommand
from src.errors.errors import NotFound, ApiError
from src.models.incident import Incident, db

class GetIncident(BaseCommand):
    def __init__(self, incident_id):
        self.incident_id = incident_id

    def execute(self):
        try:
            incident = Incident.query.filter_by(id=self.incident_id).first()
            if not incident:
                raise NotFound(f'Incident with id {self.incident_id} not found')

            incident_info = {
                'id': incident.id,
                'type': incident.type.name,
                'description': incident.description,
                'date': incident.date,
                'user_id': incident.user_id,
                'channel': incident.channel.name
            }

            return incident_info

        except NotFound as e:
            db.session.rollback()
            raise e
        
        except Exception as e:
            db.session.rollback()
            raise ApiError() from e
