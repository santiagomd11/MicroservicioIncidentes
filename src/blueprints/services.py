from flask import Blueprint, request, jsonify
from src.commands.ping import Ping
from src.commands.clear_database import ClearDatabase
from src.commands.create_user import CreateUser
from src.commands.get_user import GetUser
from src.commands.get_incident import GetIncident
from src.commands.get_incident_public import GetIncidentPublic
from src.commands.get_incidents import GetIncidents
from src.commands.create_incident import CreateIncident
from src.commands.search_incident import SearchIncident
from src.commands.search_incident_public import SearchIncidentPublic
from src.commands.update_incident_response import UpdateIncidentResponse

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
    command = CreateUser(json_data, "web")
    result = command.execute()
    return jsonify(result), 201

@services_bp.route('/mobile/create_user', methods=['POST'])
def create_user_mobile():
    json_data = request.get_json()
    command = CreateUser(json_data, "mobile")
    result = command.execute()
    return jsonify(result), 201

@services_bp.route('/get_user/<user_id>/<company>', methods=['GET'])
def get_user(user_id, company):
    command = GetUser(user_id, company)
    result = command.execute()
    return jsonify(result), 200
    

# Endpoints for Incident
@services_bp.route('/create_incident', methods=['POST'])
def create_incident():
    json_data = request.get_json()
    command = CreateIncident(json_data, "web")
    result = command.execute()
    return jsonify(result), 201

@services_bp.route('/mobile/create_incident', methods=['POST'])
def create_incident_mobile():
    json_data = request.get_json()
    command = CreateIncident(json_data, "mobile")
    result = command.execute()
    return jsonify(result), 201

@services_bp.route('/get_incident/<incident_id>/<company>', methods=['GET'])
def get_incident(incident_id, company):
    command = GetIncident(incident_id, company)
    result = command.execute()
    return jsonify(result), 200

# Agregar param para obtener los incidents de la campania especifica
@services_bp.route('/get_incidents/<company>', methods=['GET'])
def get_incidents(company):
    command = GetIncidents(company)
    result = command.execute()
    return jsonify(result), 200

@services_bp.route('/public/get_incident/<incident_id>', methods=['GET'])
def get_incident_public(incident_id):
    command = GetIncidentPublic(incident_id)
    result = command.execute()
    return jsonify(result), 200


@services_bp.route('/search_incident', methods=['POST'])
def search_incident():
    json_data = request.get_json()
    command = SearchIncident(json_data, "web")
    result = command.execute()
    return jsonify(result), 200

@services_bp.route('/mobile/search_incident', methods=['POST'])
def search_incident_mobile():
    json_data = request.get_json()
    command = SearchIncident(json_data, "mobile")
    result = command.execute()
    return jsonify(result), 200

@services_bp.route('/public/search_incident', methods=['POST'])
def search_incident_public():
    json_data = request.get_json()
    command = SearchIncidentPublic(json_data, "web")
    result = command.execute()
    return jsonify(result), 200

# Endpoint to update incident response
@services_bp.route('/update_incident_response', methods=['PUT'])
def update_incident_response():
    json_data = request.get_json()
    command = UpdateIncidentResponse(json_data)
    result = command.execute()
    return jsonify(result), 200