# services/resource_manager.py

from collections import Counter
from datetime import datetime
from typing import List, Optional

from models.incident import Incident
from models.resource import Resource
from utils.helpers import calculate_zone_distance


def _is_resource_type_allocated(incident: Incident, resource_type_str: str) -> bool:
    """
    Checks if a resource of the given type is already allocated to the incident.

    :param incident: Incident object
    :param resource_type_str: String representing the resource type
    :return: True if allocated, False otherwise
    """
    return any(r.resource_type.value == resource_type_str for r in incident.allocated_resources)


class ResourceManager:
    """
    Core service that manages emergency incidents and resources.
    Implements allocation and reallocation logic using observer-like behavior.
    """

    def __init__(self):
        """
        Initializes the resource manager with empty lists of incidents and resources.
        """
        self.incidents: List[Incident] = []
        self.resources: List[Resource] = []

    def add_incident(self, incident: Incident) -> None:
        """
        Adds a new incident to the system and triggers allocation.
        """
        self.incidents.append(incident)
        self._notify_incident_added(incident)

    def add_resource(self, resource: Resource) -> None:
        """
        Adds a new resource to the system.
        """
        self.resources.append(resource)

    def _notify_incident_added(self, incident: Incident) -> None:
        """
        Observer-style method called whenever a new incident is added.
        Triggers reallocation logic if necessary.
        """
        print(f"\n[INFO] New incident reported (Priority: {incident.priority})")
        self.allocate_resources()

    def allocate_resources(self) -> None:
        """
        Attempts to allocate available resources to pending incidents.
        Priority is given to high-priority incidents.
        """
        # Sort incidents by priority (high to low)
        sorted_incidents = sorted(
        self.incidents,
        key=lambda i: (-i.priority.value, i.timestamp)  #  First by priority desc, then by timestamp asc
        )


        for incident in sorted_incidents:
            if incident.status == "Resolved":
                continue

            for required_type in incident.required_resources:
                if not _is_resource_type_allocated(incident, required_type):
                    resource = self._find_available_resource(required_type, incident.location)
                    if resource:
                        incident.allocated_resources.append(resource)
                        resource.assign_to_incident(incident.incident_id)
                        distance = calculate_zone_distance(resource.location, incident.location)
                        print(
                            f"[ALLOCATED] {resource.resource_type} from {resource.location} "
                            f"→ Incident {incident.incident_id} ({incident.location}) "
                            f"[Distance: {distance} zone(s)]"
                        )

                    else:
                        print(f"[WAITING] No available {required_type} for Incident {incident.incident_id}")

            # Update incident status if all resources are fulfilled
            if incident.is_fulfilled():
                incident.update_status("In Progress")

    def _find_available_resource(self, resource_type_str: str, incident_location: str) -> Optional[Resource]:
        """
        Finds the closest available resource of the given type.

        :param resource_type_str: Resource type as a string (e.g., 'Ambulance')
        :param incident_location: Incident location to compare proximity
        :return: Closest available Resource or None
        """
        available_resources = [
            r for r in self.resources
            if r.resource_type.value == resource_type_str and r.is_available
        ]

        if not available_resources:
            return None

        # Find the closest resource by zone distance
        closest = min(available_resources, key=lambda r: calculate_zone_distance(r.location, incident_location))
        return closest

    def release_resources_from_resolved(self) -> None:
        """
        Releases all resources from resolved incidents, making them available again.
        """
        for incident in self.incidents:
            if incident.status == "Resolved":
                for resource in incident.allocated_resources:
                    resource.release()
                incident.allocated_resources.clear()

    def get_all_incidents(self) -> List[Incident]:
        """
        Returns a list of all recorded incidents.
        """
        return self.incidents

    def get_all_resources(self) -> List[Resource]:
        """
        Returns a list of all managed resources.
        """
        return self.resources

    def generate_summary_report(
        self,
        export: bool = False,
        status_filter: Optional[str] = None,
        zone_filter: Optional[str] = None,
        priority_filter: Optional[str] = None
    ) -> None:
        """
        Generates a dashboard summary with optional filters.

        :param export: If True, saves the summary to a text file.
        :param status_filter: Filter by incident status (Pending, In Progress, Resolved).
        :param zone_filter: Filter by zone (e.g., 'Zone 1').
        :param priority_filter: Filter by priority (High, Medium, Low).
        """
        report_lines = ["===== DASHBOARD SUMMARY ====="]

        # Apply filters
        filtered_incidents = self.incidents
        if status_filter:
            filtered_incidents = [i for i in filtered_incidents if i.status.lower() == status_filter.lower()]
        if zone_filter:
            filtered_incidents = [i for i in filtered_incidents if i.location.lower() == zone_filter.lower()]
        if priority_filter:
            filtered_incidents = [i for i in filtered_incidents if i.priority.name.lower() == priority_filter.lower()]

        report_lines.append(f"\n Filters Applied: "
                            f"{status_filter or 'All'} / {zone_filter or 'All'} / {priority_filter or 'All'}")

        # Generate summary from filtered list
        total = len(filtered_incidents)
        status_count = Counter(i.status for i in filtered_incidents)
        priority_count = Counter(i.priority.name for i in filtered_incidents)
        zone_count = Counter(i.location for i in filtered_incidents)

        report_lines.append(f"\n Total Filtered Incidents: {total}")
        for status in ["Pending", "In Progress", "Resolved"]:
            report_lines.append(f"   - {status:<11}: {status_count.get(status, 0)}")

        report_lines.append("\n Incident Priorities:")
        for p, count in priority_count.items():
            report_lines.append(f"   - {p.capitalize():<8}: {count}")

        report_lines.append("\n Incidents per Zone:")
        for zone, count in sorted(zone_count.items()):
            report_lines.append(f"   - {zone:<10}: {count}")

        total_resources = len(self.resources)
        available = sum(1 for r in self.resources if r.is_available)
        assigned = total_resources - available

        report_lines.append(f"\n Resources: {total_resources}")
        report_lines.append(f"   - Available : {available}")
        report_lines.append(f"   - Assigned  : {assigned}")
        report_lines.append("==============================")

        for line in report_lines:
            print(line)

        if export:
            with open("dashboard_summary.txt", "w") as f:
                f.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("\n".join(report_lines))
            print("[INFO] Dashboard exported to 'dashboard_summary.txt'")


