from src.commands.base_command import BaseCommand
from src.errors.errors import NotFound, ApiError, BadRequest
from src.models.incident import Incident, db

class UpdateIncidentResponse(BaseCommand):
    def __init__(self, json):
        self.incident_id = json.get('incidentId', '')
        self.company = json.get('company', '')
        self.response = json.get('response', '')

    def execute(self):
        if not self.incident_id:
            raise BadRequest('Incident id is required')
        
        if not self.response:
            raise BadRequest('Response is required')
        
        if not self.company:
            raise BadRequest('Company is required')
        
        try:
            incident = Incident.query.filter_by(id=self.incident_id, company=self.company).first()
            
            if not incident:
                raise NotFound(f'Incident with id {self.incident_id} not found')

            incident.response = self.response
            db.session.commit()

            return {
                'id': incident.id,
                'response': incident.response
            }
            
        except NotFound as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise ApiError() from e