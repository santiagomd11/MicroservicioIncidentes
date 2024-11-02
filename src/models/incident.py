import enum
import uuid
from datetime import datetime
from src.models import db

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Type(enum.Enum):
    PETICION = 1
    QUEJA = 2
    RECLAMO = 3
    SUGERENCIA = 4

class Channel(enum.Enum):
    WEB = 1 
    MOBILE = 2

class Incident(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    type = db.Column(db.Enum(Type), default=Type.PETICION)
    channel = db.Column(db.Enum(Channel), default=Channel.WEB)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    agent_id = db.Column(db.String, nullable=False)
    company = db.Column(db.String, default='')
    solved = db.Column(db.Boolean, default=False)
    
class EnumToDictionary(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}


class IncidentSchema(SQLAlchemyAutoSchema):
    type = EnumToDictionary(attribute=('type'))
    channel = EnumToDictionary(attribute=('channel'))
    
    class Meta:
        model = Incident
        include_relationships = True
        load_instance = True