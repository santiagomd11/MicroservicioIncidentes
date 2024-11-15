from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest, PreconditionFailed, NotFound
from src.models.incident import Incident, db, Type, Channel
from src.models.user import User
import uuid
import datetime

class CreateIncident(BaseCommand):
    def __init__(self, json, origin_request):
        self.id = json.get('id', str(uuid.uuid4()))
        self.type = json.get('type', Type.PETICION)
        self.description = json.get('description', '').strip()
        self.date = json.get('date', datetime.datetime.now())
        self.user_id = json.get('userId', '').strip()
        self.channel = json.get('channel', Channel.WEB)
        self.agent_id = json.get('agentId', '')
        self.company = json.get('company', '')
        self.solved = json.get('solved', False)

    def execute(self):
        if not self.description:
            raise BadRequest('Description is required')

        if not self.user_id:
            raise BadRequest('User ID is required')

        if not self.type:
            raise BadRequest('Type is required')

        if not self.date:
            raise BadRequest('Date is required')

        if not self.channel:
            raise BadRequest('Channel is required')
        
        if not self.agent_id:
            raise BadRequest('Agent ID is required')
        
        if not self.company:
            raise BadRequest('Company is required')
              
        try:
            user = User.query.filter_by(id=self.user_id).first()
            if not user:
                raise NotFound(f'User with id {self.user_id} not found')

            incident = Incident(
                id=self.id,
                type=self.type,
                description=self.description,
                date=self.date,
                user_id=self.user_id,
                channel=self.channel,
                agent_id=self.agent_id,
                company=self.company
            )

            db.session.add(incident)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise PreconditionFailed('Error creating incident, verify the data or if the incident already exists')
        
        return {"id": self.id, "description": self.description, "userEmail": user.email}