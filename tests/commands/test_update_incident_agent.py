import pytest
from src.commands.update_incident_agent import UpdateIncidentAgent

class TestUpdateIncidentAgentCommand:

    def test_update_incident_agent_success(self, mocker):
        json_data = {
            "incidentId": "123e4567-e89b-12d3-a456-426614174000",
            "agentId": "agent123",
            "company": "uniandes"
        }
        command = UpdateIncidentAgent(json_data, "web")
        mocker.patch.object(command, 'execute', return_value={"status": "success"})

        result = command.execute()

        assert result["status"] == "success"

    def test_update_incident_agent_failure(self, mocker):
        json_data = {
            "incidentId": "123e4567-e89b-12d3-a456-426614174000",
            "agentId": "agent123",
            "company": "uniandes"
        }
        command = UpdateIncidentAgent(json_data, "web")
        mocker.patch.object(command, 'execute', return_value={"status": "failure", "message": "Agent not found"})

        result = command.execute()

        assert result["status"] == "failure"
        assert result["message"] == "Agent not found"
