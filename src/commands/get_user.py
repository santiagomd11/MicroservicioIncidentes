from src.commands.base_command import BaseCommand
from src.errors.errors import NotFound, ApiError
from src.models.user import User, db

class GetUser(BaseCommand):
    def __init__(self, user_id, company):
        self.user_id = user_id
        self.company = company

    def execute(self):
        try:
            user = User.query.filter_by(id=self.user_id, company=self.company).first()
            if not user:
                raise NotFound(f'User with id {self.user_id} not found')

            user_info = {
                'id': user.id,
                'name': user.name,
                'phone': user.phone,
                'email': user.email,
                'incidents': [
                    {
                        'id': incident.id,
                        'type': incident.type.name,
                        'description': incident.description,
                        'date': incident.date,
                        'channel': incident.channel.name,
                        'agentId': incident.agent_id,
                        'company': incident.company,
                        'solved': incident.solved
                    }
                    for incident in user.incidents
                ]
            }

            return user_info
        
        except NotFound as e:
            db.session.rollback()
            raise e

        except Exception as e:
            db.session.rollback()
            raise ApiError()