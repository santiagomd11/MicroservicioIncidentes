from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest, PreconditionFailed
from src.models.user import User, db
import uuid

class CreateUser(BaseCommand):
    def __init__(self, json, origin_request):
        self.id = json.get('id', '')
        self.name = json.get('name', '').strip()
        self.phone = json.get('phone', '').strip()
        self.email = json.get('email', '').strip()
        self.company = json.get('company', '').strip()

    def execute(self):
        if not self.id:
            raise BadRequest('Id is required')
        
        if not self.name:
            raise BadRequest('Name is required')

        if not self.phone:
            raise BadRequest('Phone is required')

        if not self.email:
            raise BadRequest('Email is required')

        if not self.company:
            raise BadRequest('Company is required')

        try:
            user = User(
                id=self.id,
                name=self.name,
                phone=self.phone,
                email=self.email,
                company=self.company
            )

            db.session.add(user)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise PreconditionFailed('Error creating user, verify the data or if the user already exists') 
        
        return {"id": self.id, "name": self.name, "phone": self.phone, "email": self.email}