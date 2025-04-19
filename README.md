
```markdown
# Emergency Resource Allocation System (Console App)

A modular, object-oriented desktop application designed to simulate and optimize emergency resource allocation in real-time crisis scenarios.

---

## Features

- Log and manage emergency incidents (location, type, priority, required resources)
- Add and track resources (ambulance, fire truck, etc.)
- Priority-based allocation algorithm (High > Medium > Low)
- Proximity-based resource dispatch using simulated zone distances
- Dynamic reallocation based on incident resolution
- Real-time dashboard summary + optional export to `.txt`
- Persistent state using JSON (load on start, save on exit)
- Console-based user interface with filterable reports
- Fully modular with SOLID principles, MVC architecture, and unit testing

---

## Architecture Overview

### Modules

| Layer      | Description |
|------------|-------------|
| `models/`  | Data classes: `Incident`, `Resource`, `enums.py` |
| `services/`| Core logic: `ResourceManager` handles allocation |
| `utils/`   | Utilities: object factories, JSON I/O, zone helpers |
| `tests/`   | Unit tests using `unittest` for all components |
| `main.py`  | Console interface — interactive CLI for coordinators |

### Design Patterns

- **Factory Pattern** – `IncidentFactory`, `ResourceFactory`
- **Observer Pattern** – React to incident creation with auto-allocation
- **MVC Architecture** – Clear separation of model, logic, and view

---

## OOP Design & Principles

| Principle        | Implementation |
|------------------|----------------|
| Abstraction      | Exposed high-level methods for external use |
| Encapsulation    | State managed through internal methods |
| Polymorphism     | Enum string overrides, extensible class methods |
| Inheritance      | Resource/Incident classes are extensible |
| Modularity       | Code split into focused, reusable modules |
| SOLID Principles | Full adherence in structure and responsibilities |

---

## Requirements Met

- [x] Console-based interface with full control flow
- [x] Incident/resource creation, viewing, updating
- [x] Resource allocation + smart reallocation
- [x] Prioritization and proximity-based dispatching
- [x] Persistent storage (load/save to JSON)
- [x] Dashboard with summary + filtered reports
- [x] Unit tested with `unittest` (run via `python -m unittest discover tests`)
- [x] Class/UML diagram using Mermaid syntax
- [x] Follows SDLC practices and object-oriented software design

---

## Testing

Run all tests:

```bash
python -m unittest discover tests
```

Test files include:

- `test_models.py` – Resource & Incident behavior
- `test_resource_manager.py` – Allocation & reassignment logic
- `test_edge_cases.py` – Failures & edge scenarios
- `test_helpers.py` – Distance logic

---

## Dashboard Export

Use option `9` in the menu to export a full system summary to `dashboard_summary.txt` (with filters optional in option `10`).

---

## 📁 Project Structure

```bash
emergency_allocator/
├── main.py
├── models/
│   ├── incident.py
│   ├── resource.py
│   └── enums.py
├── services/
│   └── resource_manager.py
├── utils/
│   ├── factory.py
│   ├── helpers.py
│   └── persistence.py
├── tests/
│   ├── test_models.py
│   ├── test_resource_manager.py
│   ├── test_edge_cases.py
│   └── test_helpers.py
├── data/
│   ├── incidents.json
│   └── resources.json
├── dashboard_summary.txt  # (Generated)
└── README.md
```

---

## 👨‍💻 How to Run

```bash
python main.py
```
```

