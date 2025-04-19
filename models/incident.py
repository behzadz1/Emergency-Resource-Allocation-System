# models/incident.py

from models.enums import PriorityLevel
from typing import List
from datetime import datetime


class Incident:
    """
    Represents an emergency incident that requires one or more resources.
    """

    def __init__(
        self,
        incident_id: int,
        location: str,
        emergency_type: str,
        priority: PriorityLevel,
        required_resources: List[str]
    ):
        """
        Initializes a new incident.

        :param incident_id: Unique identifier for the incident.
        :param location: A string representing the location (e.g., 'Zone 1').
        :param emergency_type: Description of the type of emergency (e.g., 'Fire').
        :param priority: PriorityLevel enum indicating the urgency of the incident.
        :param required_resources: List of resource types required (as strings).
        """
        self.incident_id = incident_id
        self.location = location
        self.emergency_type = emergency_type
        self.priority = priority
        self.required_resources = required_resources
        self.allocated_resources = []  # Stores resources assigned to this incident
        self.status = "Pending"  # Can be 'Pending', 'In Progress', 'Resolved'
        self.timestamp = datetime.now() #  When the incident was created

    def is_fulfilled(self) -> bool:
        """
        Checks whether all required resources have been allocated.

        :return: True if all resources are allocated, False otherwise.
        """
        return len(self.allocated_resources) >= len(self.required_resources)

    def update_status(self, new_status: str) -> None:
        """
        Updates the current status of the incident.

        :param new_status: A new status string ('Pending', 'In Progress', 'Resolved').
        """
        self.status = new_status

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the incident.
        """
        return (
            f"Incident ID: {self.incident_id} | Location: {self.location} | "
            f"Type: {self.emergency_type} | Priority: {self.priority} | "
            f"Status: {self.status} | Required: {self.required_resources} | "
            f"Allocated: {[str(r) for r in self.allocated_resources]}"
            f"Time: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )
