from flask import Blueprint, request, jsonify
from src.commands.ping import Ping
from src.commands.clear_database import ClearDatabase
from src.commands.create_user import CreateUser
from src.commands.get_user import GetUser
from src.commands.get_incident import GetIncident
from src.commands.get_incidents import GetIncidents
from src.commands.create_incident import CreateIncident
from src.commands.search_incident import SearchIncident

from src.errors.errors import BadRequest, NotFound

services_bp = Blueprint('services', __name__)

@services_bp.route('/clear_database', methods=['POST'])
def clear_database():
    command = ClearDatabase()
    command.execute()
    return jsonify({'message': 'Database cleared successfully'}), 200

@services_bp.route('/ping', methods=['GET'])
def ping():
    command = Ping()
    return jsonify({'message': command.execute()}), 200

# Endpoints for User

@services_bp.route('/create_user', methods=['POST'])
def create_user():
    json_data = request.get_json()
    command = CreateUser(json_data)
    result = command.execute()
    return jsonify(result), 201

@services_bp.route('/get_user/<user_id>', methods=['GET'])
def get_user(user_id):
    command = GetUser(user_id)
    result = command.execute()
    return jsonify(result), 200
    

# Endpoints for Incident

@services_bp.route('/create_incident', methods=['POST'])
def create_incident():
    json_data = request.get_json()
    command = CreateIncident(json_data)
    result = command.execute()
    return jsonify(result), 201

@services_bp.route('/get_incident/<incident_id>', methods=['GET'])
def get_incident(incident_id):
    command = GetIncident(incident_id)
    result = command.execute()
    return jsonify(result), 200

@services_bp.route('/get_incidents', methods=['GET'])
def get_incidents():
    command = GetIncidents()
    result = command.execute()
    return jsonify(result), 200


@services_bp.route('/search_incident', methods=['POST'])
def search_incident():
    json_data = request.get_json()
    command = SearchIncident(json_data)
    result = command.execute()
    return jsonify(result), 200