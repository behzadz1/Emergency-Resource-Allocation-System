# models/resource.py

from models.enums import ResourceType


class Resource:
    """
    Represents an emergency response resource such as an ambulance or medical team.
    """

    def __init__(
        self,
        resource_id: int,
        resource_type: ResourceType,
        location: str,
        is_available: bool = True
    ):
        """
        Initializes a new resource.

        :param resource_id: Unique identifier for the resource.
        :param resource_type: Type of the resource (e.g., ambulance, fire truck).
        :param location: The current location of the resource (e.g., 'Zone 1').
        :param is_available: Availability status of the resource.
        """
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.location = location
        self.is_available = is_available
        self.assigned_to_incident = None  # Track incident ID if assigned

    def assign_to_incident(self, incident_id: int) -> None:
        """
        Marks the resource as assigned to an incident.

        :param incident_id: ID of the incident the resource is assigned to.
        """
        self.is_available = False
        self.assigned_to_incident = incident_id

    def release(self) -> None:
        """
        Releases the resource back to available pool (e.g., after resolving an incident).
        """
        self.is_available = True
        self.assigned_to_incident = None

    def __str__(self) -> str:
        """
        Returns a string representation of the resource for display purposes.
        """
        status = "Available" if self.is_available else f"Assigned to Incident {self.assigned_to_incident}"
        return (
            f"Resource ID: {self.resource_id} | Type: {self.resource_type} | "
            f"Location: {self.location} | Status: {status}"
        )
