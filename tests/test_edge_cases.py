# tests/test_edge_cases.py

import unittest
from services.resource_manager import ResourceManager
from models.incident import Incident
from models.resource import Resource
from models.enums import PriorityLevel, ResourceType


class TestEdgeCases(unittest.TestCase):

    def setUp(self):
        self.manager = ResourceManager()

    def test_no_resources_available(self):
        """
        Verify that an incident remains unfulfilled when no resources exist.
        """
        incident = Incident(
            incident_id=1,
            location="Zone X",
            emergency_type="Flood",
            priority=PriorityLevel.HIGH,
            required_resources=["Ambulance"]
        )
        self.manager.add_incident(incident)
        self.manager.allocate_resources()

        self.assertEqual(incident.status, "Pending")
        self.assertEqual(len(incident.allocated_resources), 0)

    def test_multiple_high_priority_incidents_with_one_resource(self):
        """
        Ensure that only the first high-priority incident gets the resource.
        """
        resource = Resource(1, ResourceType.AMBULANCE, "Zone 1")
        self.manager.add_resource(resource)

        # Two incidents needing the same resource
        incident1 = Incident(1, "Zone 1", "Crash", PriorityLevel.HIGH, ["Ambulance"])
        incident2 = Incident(2, "Zone 1", "Explosion", PriorityLevel.HIGH, ["Ambulance"])

        self.manager.add_incident(incident1)
        self.manager.add_incident(incident2)
        self.manager.allocate_resources()

        self.assertEqual(len(incident1.allocated_resources), 1)
        self.assertEqual(len(incident2.allocated_resources), 0)
        self.assertEqual(incident1.status, "In Progress")
        self.assertEqual(incident2.status, "Pending")

    def test_incident_with_multiple_required_resources_partial_availability(self):
        """
        Incident has multiple resource needs but only some are available.
        Status should remain pending.
        """
        ambulance = Resource(1, ResourceType.AMBULANCE, "Zone 1")
        self.manager.add_resource(ambulance)

        incident = Incident(1, "Zone 1", "Large Fire", PriorityLevel.HIGH, ["Ambulance", "Fire Truck"])
        self.manager.add_incident(incident)
        self.manager.allocate_resources()

        self.assertEqual(len(incident.allocated_resources), 1)
        self.assertEqual(incident.status, "Pending")  # Should not be marked In Progress yet

    def test_invalid_resource_type_allocation(self):
        """
        System should not crash if an unknown resource type is requested.
        """
        unknown_type_incident = Incident(
            incident_id=3,
            location="Zone 3",
            emergency_type="Unknown Emergency",
            priority=PriorityLevel.MEDIUM,
            required_resources=["Dragon"]  # Non-existent resource type
        )

        self.manager.add_incident(unknown_type_incident)
        try:
            self.manager.allocate_resources()
            self.assertTrue(True)  # No crash
        except Exception as e:
            self.fail(f"Allocation raised an exception: {e}")

        self.assertEqual(unknown_type_incident.status, "Pending")
        self.assertEqual(len(unknown_type_incident.allocated_resources), 0)


if __name__ == "__main__":
    unittest.main()

