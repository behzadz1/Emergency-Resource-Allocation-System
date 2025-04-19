# tests/test_resource_manager.py

import unittest
from services.resource_manager import ResourceManager
from models.incident import Incident
from models.resource import Resource
from models.enums import PriorityLevel, ResourceType


class TestResourceManager(unittest.TestCase):

    def setUp(self):
        self.manager = ResourceManager()

        # Create resources
        self.ambulance = Resource(1, ResourceType.AMBULANCE, "Zone 1")
        self.fire_truck = Resource(2, ResourceType.FIRE_TRUCK, "Zone 1")
        self.manager.add_resource(self.ambulance)
        self.manager.add_resource(self.fire_truck)

        # Create incidents
        self.incident1 = Incident(
            incident_id=101,
            location="Zone 1",
            emergency_type="Accident",
            priority=PriorityLevel.HIGH,
            required_resources=["Ambulance"]
        )
        self.incident2 = Incident(
            incident_id=102,
            location="Zone 1",
            emergency_type="Fire",
            priority=PriorityLevel.LOW,
            required_resources=["Fire Truck"]
        )

    def test_add_incident_and_resource(self):
        self.manager.add_incident(self.incident1)
        self.assertEqual(len(self.manager.get_all_incidents()), 1)
        self.assertEqual(len(self.manager.get_all_resources()), 2)

    def test_resource_allocation_priority(self):
        # Add both incidents, high priority first
        self.manager.add_incident(self.incident1)
        self.manager.add_incident(self.incident2)

        self.manager.allocate_resources()

        # High-priority incident should get ambulance
        self.assertEqual(len(self.incident1.allocated_resources), 1)
        self.assertEqual(self.incident1.status, "In Progress")

        # Low-priority incident should also get fire truck
        self.assertEqual(len(self.incident2.allocated_resources), 1)
        self.assertEqual(self.incident2.status, "In Progress")

    def test_resource_allocation_when_not_available(self):
        # Assign ambulance to first incident
        self.manager.add_incident(self.incident1)
        self.manager.allocate_resources()

        # Create another high-priority incident needing ambulance
        incident3 = Incident(
            incident_id=103,
            location="Zone 1",
            emergency_type="Heart Attack",
            priority=PriorityLevel.HIGH,
            required_resources=["Ambulance"]
        )
        self.manager.add_incident(incident3)
        self.manager.allocate_resources()

        # The second incident should not receive the ambulance since it's already used
        self.assertEqual(len(incident3.allocated_resources), 0)
        self.assertEqual(incident3.status, "Pending")

    def test_resolve_and_reallocate(self):
        # Allocate ambulance to first incident
        self.manager.add_incident(self.incident1)
        self.manager.allocate_resources()

        # Resolve first incident
        self.incident1.update_status("Resolved")
        self.manager.release_resources_from_resolved()

        self.assertTrue(self.ambulance.is_available)

        # Add another incident needing ambulance
        new_incident = Incident(
            incident_id=104,
            location="Zone 1",
            emergency_type="Burn",
            priority=PriorityLevel.HIGH,
            required_resources=["Ambulance"]
        )
        self.manager.add_incident(new_incident)
        self.manager.allocate_resources()

        self.assertEqual(len(new_incident.allocated_resources), 1)
        self.assertEqual(new_incident.status, "In Progress")


if __name__ == '__main__':
    unittest.main()

