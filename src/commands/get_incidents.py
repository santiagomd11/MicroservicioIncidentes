from src.commands.base_command import BaseCommand
from src.models.incident import Incident, db

class GetIncidents(BaseCommand):
    def execute(self):
        try:
            incidents = Incident.query.all()
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