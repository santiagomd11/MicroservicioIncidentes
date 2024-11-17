from src.commands.base_command import BaseCommand
from src.models.incident import Incident, db
from src.errors.errors import NotFound, ApiError, BadRequest

class UpdateIncidentAgent(BaseCommand):
    def __init__(self, json, origin_request):
        self.incident_id = json.get('incidentId', '').strip()
        self.agent_id = json.get('agentId', '').strip()
        self.company = json.get('company', '').strip()

    def execute(self):
        try:
            incident = Incident.query.filter_by(id=self.incident_id, company=self.company).first()
            if not self.incident_id:
                raise BadRequest("Incident id is required")
            if not self.agent_id:
                raise BadRequest("Agent id is required")
            if not self.company:
                raise BadRequest("Company is required")
            if not incident:
                raise NotFound("El incidente no fue encontrado")

            incident.agent_id = self.agent_id
            db.session.commit()

            return {
                'id': incident.id,
                'agentId': incident.agent_id,
                'message': 'Agent updated successfully'
            }
        except Exception as e:
            db.session.rollback()
            raise ApiError(f"Error updating agent: {str(e)}")