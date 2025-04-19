# utils/factory.py

from models.incident import Incident
from models.resource import Resource
from models.enums import PriorityLevel, ResourceType
from typing import List


class IncidentFactory:
    """
    Factory for creating Incident objects.
    Responsible for converting user input into structured Incident instances.
    """

    _incident_counter = 1  # Internal counter to auto-generate unique incident IDs

    @classmethod
    def create_incident(
        cls,
        location: str,
        emergency_type: str,
        priority_str: str,
        required_resource_names: List[str]
    ) -> Incident:
        """
        Creates and returns a new Incident object.

        :param location: Location of the incident (e.g., 'Zone 3').
        :param emergency_type: Description of the emergency (e.g., 'Accident').
        :param priority_str: Priority as a string (e.g., 'High').
        :param required_resource_names: List of resource type strings.
        :return: Incident object.
        """
        priority = PriorityLevel[priority_str.upper()]
        incident_id = cls._incident_counter
        cls._incident_counter += 1

        return Incident(
            incident_id=incident_id,
            location=location,
            emergency_type=emergency_type,
            priority=priority,
            required_resources=required_resource_names
        )


class ResourceFactory:
    """
    Factory for creating Resource objects.
    Simplifies creation and ensures consistent ID assignment.
    """

    _resource_counter = 1  # Internal counter to auto-generate unique resource IDs

    @classmethod
    def create_resource(cls, resource_type_str: str, location: str) -> Resource:
        """
        Creates and returns a new Resource object.

        :param resource_type_str: Type of the resource as a string (e.g., 'Ambulance').
        :param location: Initial location of the resource (e.g., 'Zone 2').
        :return: Resource object.
        """
        resource_type_enum = ResourceType(resource_type_str.title())
        resource_id = cls._resource_counter
        cls._resource_counter += 1

        return Resource(
            resource_id=resource_id,
            resource_type=resource_type_enum,
            location=location
        )
