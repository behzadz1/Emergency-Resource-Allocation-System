# UML Class Diagram - Emergency Resource Allocation System

This UML-style class diagram presents a structured overview of the core components in the Emergency Resource Allocation System. The diagram uses consistent formatting to improve readability and illustrates the relationships between models, services, utilities, and enums.

```
+--------------------+          +--------------------+          +----------------------+
|     <<enum>>       |          |     <<enum>>       |          |      <<class>>       |
|   PriorityLevel    |          |   ResourceType     |          |       Resource       |
+--------------------+          +--------------------+          +----------------------+
| + HIGH             |          | + AMBULANCE        |          | - resource_id: int   |
| + MEDIUM           |          | + FIRE_TRUCK       |          | - resource_type      |
| + LOW              |          | + MEDICAL_TEAM     |          | - location: str      |
|                    |          | + POLICE_UNIT      |          | - is_available: bool |
+--------------------+          +--------------------+          | - assigned_to_id: int|

                                                                +-----------------------+
                                                                | + assign_to_incident()|
                                                                | + release()           |
                                                                +-----------------------+

+----------------------+                                          +--------------------------+
|      <<class>>       |                                          |       <<class>>          |
|       Incident       |                                          |   ResourceFactory        |
+----------------------+                                          +--------------------------+
| - incident_id: int   |                                          | + create_resource()      |
| - location: str      |                                          +--------------------------+
| - emergency_type     |
| - priority           |         +----------------------+         +--------------------------+
| - status             |         |      <<class>>       |         |        <<class>>         |
| - required_resources |<------->|       Resource       |         |    IncidentFactory       |
| - allocated_resources|         +----------------------+         +--------------------------+
| - timestamp          |                                          | + create_incident()      |
+----------------------+                                          +--------------------------+
| + update_status()    |
| + is_fulfilled()     |
+----------------------+

+----------------------------+
|        <<class>>           |
|     ResourceManager        |
+----------------------------+
| - incidents                |
| - resources                |
+----------------------------+
| + add_incident()           |
| + add_resource()           |
| + allocate_resources()     |
| + release_resources()      |
| + generate_summary_report()|
+----------------------------+

+----------------------------+
|        <<class>>           |
|        Persistence         |
+----------------------------+
| + save_data()              |
| + load_data()              |
+----------------------------+

+----------------------------+
|        <<class>>           |
|          Helpers           |
+----------------------------+
| + calculate_zone_distance()|
+----------------------------+
```

## Legend
- `<<enum>>`: Enumerated types used for classifying priority and resource types.
- `<<class>>`: Standard class definitions.
- `<------->`: Represents a many-to-many relationship between `Incident` and `Resource`.
- Member variables and methods follow Python conventions with type hints.

This diagram demonstrates the system's adherence to OOP principles, modular structure, and separation of concerns—facilitating testability, maintainability, and future extensibility.

