from src.commands.base_command import BaseCommand
from src.errors.errors import NotFound, ApiError
from src.models.incident import Incident, db

class GetIncident(BaseCommand):
    def __init__(self, incident_id, company):
        self.incident_id = incident_id
        self.company = company

    def execute(self):
        try:
            incident = Incident.query.filter_by(id=self.incident_id, company=self.company).first()
            
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

        except NotFound as e:
            db.session.rollback()
            raise e
        
        except Exception as e:
            db.session.rollback()
            raise ApiError() from e
