# main.py

from models.enums import ResourceType
from services.resource_manager import ResourceManager
from utils.factory import IncidentFactory, ResourceFactory
from utils.persistence import save_data, load_data


def display_main_menu() -> None:
    print("\n=== Emergency Resource Allocation System ===")
    print("1. Add Incident")
    print("2. Add Resource")
    print("3. View All Incidents")
    print("4. View All Resources")
    print("5. Allocate Resources")
    print("6. Resolve Incident")
    print("7. View Dashboard Summary")
    print("8. Export Dashboard Summary to File")
    print("9. Filtered Dashboard Summary")
    print("10. Exit")


def add_incident_ui(resource_manager: ResourceManager) -> None:
    try:
        location = input("Enter incident location (e.g., Zone 1): ")
        emergency_type = input("Enter emergency type (e.g., Fire, Medical): ")
        priority = input("Enter priority (High, Medium, Low): ").capitalize()

        if priority not in ["High", "Medium", "Low"]:
            print("[ERROR] Invalid priority.")
            return

        print("Available Resource Types:")
        for rt in ResourceType:
            print(f" - {rt.value}")
        required = input("Enter required resources (comma-separated, e.g., Ambulance,Fire Truck): ")
        required_resources = [r.strip().title() for r in required.split(",")]

        incident = IncidentFactory.create_incident(location, emergency_type, priority, required_resources)
        resource_manager.add_incident(incident)

        print("[SUCCESS] Incident added.")
    except Exception as e:
        print(f"[ERROR] Failed to add incident: {e}")


def add_resource_ui(resource_manager: ResourceManager) -> None:
    try:
        print("Available Resource Types:")
        for rt in ResourceType:
            print(f" - {rt.value}")
        resource_type = input("Enter resource type: ").title()
        location = input("Enter resource location (e.g., Zone 1): ")

        resource = ResourceFactory.create_resource(resource_type, location)
        resource_manager.add_resource(resource)

        print("[SUCCESS] Resource added.")
    except Exception as e:
        print(f"[ERROR] Failed to add resource: {e}")


def view_incidents(resource_manager: ResourceManager) -> None:
    incidents = resource_manager.get_all_incidents()
    if not incidents:
        print("No incidents recorded.")
        return
    for incident in incidents:
        print(incident)


def view_resources(resource_manager: ResourceManager) -> None:
    resources = resource_manager.get_all_resources()
    if not resources:
        print("No resources recorded.")
        return
    for resource in resources:
        print(resource)


def resolve_incident_ui(resource_manager: ResourceManager) -> None:
    try:
        incident_id = int(input("Enter Incident ID to resolve: "))
        for incident in resource_manager.get_all_incidents():
            if incident.incident_id == incident_id:
                incident.update_status("Resolved")
                print(f"[INFO] Incident {incident_id} marked as resolved.")
                resource_manager.release_resources_from_resolved()
                return
        print("[WARN] Incident ID not found.")
    except Exception as e:
        print(f"[ERROR] {e}")


def run():
    # === AUTO-LOAD ON STARTUP ===
    print("[SYSTEM] Loading previous state...")
    resource_manager = ResourceManager()

    # Load and inject data
    incidents = load_data("data/incidents.json", "incident")
    resources = load_data("data/resources.json", "resource")
    for incident in incidents:
        resource_manager.add_incident(incident)
    for resource in resources:
        resource_manager.add_resource(resource)

    print(f"[SYSTEM] Loaded {len(incidents)} incidents and {len(resources)} resources.")

    while True:
        display_main_menu()
        choice = input("Select an option (1-7): ").strip()
        if choice == "1":
            add_incident_ui(resource_manager)
        elif choice == "2":
            add_resource_ui(resource_manager)
        elif choice == "3":
            view_incidents(resource_manager)
        elif choice == "4":
            view_resources(resource_manager)
        elif choice == "5":
            resource_manager.allocate_resources()
        elif choice == "6":
            resolve_incident_ui(resource_manager)
        elif choice == "7":
            resource_manager.generate_summary_report()
        elif choice == "8":
            resource_manager.generate_summary_report(export=True)
        elif choice == "9":
            status = input("Filter by status (Pending/In Progress/Resolved) or leave blank: ").strip()
            zone = input("Filter by zone (e.g., Zone 1) or leave blank: ").strip()
            priority = input("Filter by priority (High/Medium/Low) or leave blank: ").strip()
            resource_manager.generate_summary_report(
                status_filter=status or None,
                zone_filter=zone or None,
                priority_filter=priority or None
            )
        elif choice == "10":
            print("[SYSTEM] Saving system state...")
            save_data("data/incidents.json", resource_manager.get_all_incidents(), "incident")
            save_data("data/resources.json", resource_manager.get_all_resources(), "resource")
            print("Exiting application. Goodbye!")
            break
        else:
            print("[ERROR] Invalid option. Please try again.")


if __name__ == "__main__":
    run()
