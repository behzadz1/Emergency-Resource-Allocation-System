# tests/test_models.py

import unittest
from models.enums import PriorityLevel, ResourceType
from models.incident import Incident
from models.resource import Resource


class TestIncident(unittest.TestCase):

    def setUp(self):
        self.incident = Incident(
            incident_id=1,
            location="Zone 1",
            emergency_type="Fire",
            priority=PriorityLevel.HIGH,
            required_resources=["Ambulance", "Fire Truck"]
        )

    def test_initial_status(self):
        self.assertEqual(self.incident.status, "Pending")

    def test_is_fulfilled_false(self):
        self.assertFalse(self.incident.is_fulfilled())

    def test_update_status(self):
        self.incident.update_status("In Progress")
        self.assertEqual(self.incident.status, "In Progress")


class TestResource(unittest.TestCase):

    def setUp(self):
        self.resource = Resource(
            resource_id=1,
            resource_type=ResourceType.AMBULANCE,
            location="Zone 2"
        )

    def test_initial_availability(self):
        self.assertTrue(self.resource.is_available)

    def test_assign_and_release(self):
        self.resource.assign_to_incident(incident_id=5)
        self.assertFalse(self.resource.is_available)
        self.assertEqual(self.resource.assigned_to_incident, 5)

        self.resource.release()
        self.assertTrue(self.resource.is_available)
        self.assertIsNone(self.resource.assigned_to_incident)


if __name__ == '__main__':
    unittest.main()

