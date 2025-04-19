# models/enums.py

from enum import Enum

class PriorityLevel(Enum):
    """
    Enum representing the priority levels of an emergency incident.
    Higher numeric value = higher priority.
    """
    HIGH = 3
    MEDIUM = 2
    LOW = 1

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the priority level.
        """
        return self.name.capitalize()


class ResourceType(Enum):
    """
    Enum representing the types of emergency response resources.
    """
    AMBULANCE = "Ambulance"
    FIRE_TRUCK = "Fire Truck"
    MEDICAL_TEAM = "Medical Team"
    POLICE_UNIT = "Police Unit"
    SEARCH_RESCUE_TEAM = "Search & Rescue Team"

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the resource type.
        """
        return self.value
