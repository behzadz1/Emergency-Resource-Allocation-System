# utils/persistence.py

import json
from models.incident import Incident
from models.resource import Resource
from datetime import datetime
from models.enums import PriorityLevel, ResourceType


def save_data(filename: str, data: list, data_type: str) -> None:
    """
    Saves a list of objects (Incidents or Resources) to a JSON file.

    :param filename: Path to the output JSON file.
    :param data: List of objects to save.
    :param data_type: Either 'incident' or 'resource'.
    """
    with open(filename, 'w') as f:
        if data_type == 'incident':
            json.dump([_incident_to_dict(i) for i in data], f, indent=4)
        elif data_type == 'resource':
            json.dump([_resource_to_dict(r) for r in data], f, indent=4)


def load_data(filename: str, data_type: str) -> list:
    """
    Loads data from a JSON file and reconstructs it as objects.

    :param filename: Path to JSON file.
    :param data_type: Either 'incident' or 'resource'.
    :return: List of reconstructed objects.
    """
    try:
        with open(filename, 'r') as f:
            raw_data = json.load(f)
            if data_type == 'incident':
                return [_dict_to_incident(d) for d in raw_data]
            elif data_type == 'resource':
                return [_dict_to_resource(d) for d in raw_data]
    except FileNotFoundError:
        return []  # Return empty list if file doesn't exist


# ------------------------ Helpers ------------------------

def _incident_to_dict(incident: Incident) -> dict:
    return {
        'incident_id': incident.incident_id,
        'location': incident.location,
        'emergency_type': incident.emergency_type,
        'priority': incident.priority.name,
        'required_resources': incident.required_resources,
        'allocated_resources': [r.resource_id for r in incident.allocated_resources],
        'status': incident.status,
        'timestamp': incident.timestamp.isoformat()
    }


def _resource_to_dict(resource: Resource) -> dict:
    return {
        'resource_id': resource.resource_id,
        'resource_type': resource.resource_type.value,
        'location': resource.location,
        'is_available': resource.is_available,
        'assigned_to_incident': resource.assigned_to_incident
    }


def _dict_to_incident(data: dict) -> Incident:
    """
    Converts a dictionary loaded from JSON into an Incident object.
    """
    incident = Incident(
        incident_id=data['incident_id'],
        location=data['location'],
        emergency_type=data['emergency_type'],
        priority=PriorityLevel[data['priority']],
        required_resources=data['required_resources']
    )
    incident.status = data['status']
    incident.timestamp = datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat()))
    return incident


def _dict_to_resource(data: dict) -> Resource:
    resource = Resource(
        resource_id=data['resource_id'],
        resource_type=ResourceType(data['resource_type']),
        location=data['location'],
        is_available=data['is_available']
    )
    resource.assigned_to_incident = data['assigned_to_incident']
    return resource

