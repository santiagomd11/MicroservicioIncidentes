from src.commands.base_command import BaseCommand
from src.models.incident import Incident, db
from src.errors.errors import ApiError

class GetIncidents(BaseCommand):
    def __init__(self, company):
        self.company = company
        
    def execute(self):
        try:
            incidents = Incident.query.filter_by(company=self.company).all()
            incidents_info = [
                {
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
                for incident in incidents
            ]

            return incidents_info

        except Exception as e:
            db.session.rollback()
            raise ApiError()