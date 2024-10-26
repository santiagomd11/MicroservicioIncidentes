from src.commands.base_command import BaseCommand
from src.errors.errors import NotFound
from src.models.user import User, db

class GetUser(BaseCommand):
    def __init__(self, user_id):
        self.user_id = user_id

    def execute(self):
        try:
            user = User.query.filter_by(id=self.user_id).first()
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
                        'chanel': incident.chanel.name
                    }
                    for incident in user.incidents
                ]
            }

            return user_info

        except Exception as e:
            db.session.rollback()
            raise e