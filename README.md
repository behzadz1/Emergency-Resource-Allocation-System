# 🚑 Emergency Resource Allocation System

A console-based Python application that manages real-time allocation of emergency resources (ambulances, fire trucks, medical teams, etc.) to incidents based on priority, proximity, and availability.

---

## 📌 Features

- Log emergency incidents with type, location, priority
- Manage available resources and their locations
- Automatically allocate resources by priority and distance
- Dynamically reallocate if a higher-priority incident arrives
- Persistent data storage with JSON (load/save)
- Console dashboard and summary reports
- Modular architecture using OOP and SOLID principles
- Unit test coverage for all major modules

---

## 🗂️ Project Structure
```
Emergency-Resource-Allocation-System-main/
├── main.py                    # Console UI entry point
├── models/                   # Data models (Incident, Resource, Enums)
├── services/                 # Business logic (ResourceManager)
├── utils/                    # Helpers, factories, persistence
├── tests/                    # Unit and edge case tests
├── data/                     # JSON storage for resources/incidents
├── dashboard_summary.txt     # Summary output
├── Diagram_UML.md            # Class diagram (ASCII/Markdown)
├── README.md                 # This file
```

---

## 🚀 How to Run

Make sure you're using Python 3.8 or newer.

```bash
cd Emergency-Resource-Allocation-System-main
python main.py
```

You’ll interact with the system via a text-based console menu.

---

## 🧪 How to Run Tests

Tests are written using the built-in `unittest` framework.

```bash
python -m unittest discover tests
```

---

## 🧩 Dependencies

This project uses only Python standard libraries:
- `datetime`
- `json`
- `os`
- `typing`

To ensure compatibility, use:
```
python >= 3.8
```

---

## 📊 UML Diagram
See `Diagram_UML.md` for the full class diagram and module relationships.

---

## 🧠 Design Principles
- Follows MVC-style separation
- Uses Factory and Observer patterns
- Applies SOLID, DRY, and KISS principles
- Modular, testable, and maintainable codebase

---

## 📂 Data Persistence
- Incident and resource data are loaded from and saved to `data/` on exit and startup.
- Format: JSON

---

## 🙌 Credits
Developed as part of a software development course and final assessment project.

