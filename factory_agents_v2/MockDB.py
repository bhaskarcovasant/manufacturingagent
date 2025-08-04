"""
Mock Database for a Reactive Smart Factory System.

This data is structured to support a maintenance workflow triggered by user reports.
The connections link user-described issues to specific parts and technician skills.
"""
from typing import Dict, Any, List

class MockDB:
    """A mock database with logically connected data for factory operations."""
    
    def __init__(self):
        """Initialize the mock database with sample data."""

        self.machines = {
            "PUMP-A-01": {
                "id": "PUMP-A-01",
                "name": "Pump System A1",
                "type": "Pump",
                "status": "operational",
                "last_maintenance": "2025-07-15T08:00:00",
                "next_maintenance": "2025-08-15T08:00:00"
            },
            "MOTOR-B-02": {
                "id": "MOTOR-B-02",
                "name": "Electric Motor B2",
                "type": "Motor",
                "status": "operational",
                "last_maintenance": "2025-07-10T14:00:00",
                "next_maintenance": "2025-08-10T14:00:00"
            },
            "TURBINE-C-01": {
                "id": "TURBINE-C-01",
                "name": "Turbine C1",
                "type": "Turbine",
                "status": "operational",
                "last_maintenance": "2025-07-20T09:30:00",
                "next_maintenance": "2025-08-20T09:30:00"
            },
            "COMPRESSOR-D-04": {
                "id": "COMPRESSOR-D-04",
                "name": "Air Compressor D4",
                "type": "Compressor",
                "status": "operational",
                "last_maintenance": "2025-07-05T10:00:00",
                "next_maintenance": "2025-08-05T10:00:00"
            },
            "GEARBOX-F-03": {
                "id": "GEARBOX-F-03",
                "name": "Gearbox System F3",
                "type": "Gearbox",
                "status": "operational",
                "last_maintenance": "2025-07-12T11:00:00",
                "next_maintenance": "2025-08-12T11:00:00"
            },
            "HVAC-G-11": {
                "id": "HVAC-G-11",
                "name": "HVAC System G11",
                "type": "HVAC",
                "status": "operational",
                "last_maintenance": "2025-07-18T08:30:00",
                "next_maintenance": "2025-08-18T08:30:00"
            },
            "ROBOT-J-15": {
                "id": "ROBOT-J-15",
                "name": "Robotic Arm J15",
                "type": "Robot",
                "status": "maintenance",
                "last_maintenance": "2025-08-01T08:00:00",
                "next_maintenance": "2025-09-01T08:00:00"
            }
        }

        self.machine_details = {
            "PUMP-A-01": {
                "id": "PUMP-A-01",
                "temperature": 70.5,  # Normal range: 50-80°C
                "vibration": 1.48,    # Normal range: 0.5-3.0 mm/s
                "pressure": 301.5,    # Normal for this pump type
                "timestamp": "2024-08-02 08:00:00"
            },
            "MOTOR-B-02": {
                "id": "MOTOR-B-02",
                "temperature": 92.3,  # Above normal range: 50-80°C
                "vibration": 8.7,     # Much higher than normal (0.5-3.0 mm/s)
                "pressure": 145.2,    # Within normal range
                "timestamp": "2024-08-02 08:10:00"
            },
            "TURBINE-C-01": {
                "id": "TURBINE-C-01",
                "temperature": 152.5,  # Normal for turbine (high temperature equipment)
                "vibration": 0.83,    # Normal vibration
                "pressure": 501.4,     # Normal pressure for this turbine
                "timestamp": "2024-08-02 08:10:00"
            },
            "COMPRESSOR-D-04": {
                "id": "COMPRESSOR-D-04",
                "temperature": 85.4,   # Slightly above normal range
                "vibration": 3.15,    # At the upper limit of normal
                "pressure": 211.0,     # Normal pressure for compressor
                "timestamp": "2024-08-02 08:05:00"
            },
            "GEARBOX-F-03": {
                "id": "GEARBOX-F-03",
                "temperature": 96.1,   # Above normal range
                "vibration": 8.1,      # Much higher than normal
                "pressure": 174.5,     # Within normal range
                "timestamp": "2024-08-02 08:15:00"
            },
            "HVAC-G-11": {
                "id": "HVAC-G-11",
                "temperature": 55.3,   # Within normal range
                "vibration": 1.11,    # Within normal range
                "pressure": 125.6,     # Within normal range
                "timestamp": "2024-08-02 08:15:00"
            },
            "ROBOT-J-15": {
                "id": "ROBOT-J-15",
                "temperature": 65.8,   # Within normal range
                "vibration": 0.95,    # Within normal range
                "pressure": 100.3,     # Within normal range
                "timestamp": "2024-08-02 08:20:00"
            }
        }

        self.inventory: Dict[str, Dict[str, Any]] = {
            "part-brg-001": {
                "id": "part-brg-001",
                "name": "Standard Bearing Assembly",
                "keywords": ["bearing", "grinding", "vibration", "noise", "high vibration"],
                "quantity": 12,
                "location": "Warehouse A, Bin 3",
                "applicable_machine_types": ["Motor", "Pump", "Gearbox"] 
            },
            "part-pmp-seal-004": {
                "id": "part-pmp-seal-004",
                "name": "Seal Kit",
                "keywords": ["seal", "leaking", "leak", "fluid loss"],
                "quantity": 25,
                "location": "Warehouse C, Bin 1",
                "applicable_machine_types": ["Pump", "Gearbox"]
            },
            "part-gr-set-007": {
                "id": "part-gr-set-007",
                "name": "Primary Gear Set",
                "keywords": ["gear", "slipping", "jammed", "broken tooth", "grinding"],
                "quantity": 0, # Intentionally out of stock to test failure paths.
                "location": "Warehouse B, Bin 8",
                "applicable_machine_types": ["Gearbox"]
            },
            
            "part-cmp-flt-012": {
                "id": "part-cmp-flt-012",
                "name": "Compressor Air Filter",
                "keywords": ["filter", "clogged", "overheating", "temperature", "pressure drop"],
                "quantity": 40,
                "location": "Warehouse C, Bin 2",
                "applicable_machine_types": ["Compressor"]
            },
            "part-trb-bld-003": {
                "id": "part-trb-bld-003",
                "name": "High-Stress Turbine Blade",
                "keywords": ["blade", "turbine", "fatigue", "imbalance", "catastrophic failure"],
                "quantity": 8,
                "location": "Warehouse B, Secure Cage",
                "applicable_machine_types": ["Turbine"]
            },
            "part-hvc-flt-001": {
                "id": "part-hvc-flt-001",
                "name": "Industrial HVAC Filter Cartridge",
                "keywords": ["hvac", "filter", "air flow", "dusty", "clogged"],
                "quantity": 150,
                "location": "General Storage, Shelf D",
                "applicable_machine_types": ["HVAC"]
            },
            "part-rbt-srv-009": {
                "id": "part-rbt-srv-009",
                "name": "Axis 4 Servo Motor",
                "keywords": ["robot", "servo", "motor", "joint", "axis", "not moving", "fault"],
                "quantity": 6,
                "location": "Electronics Lab, Shelf 3",
                "applicable_machine_types": ["Robot"]
            },
            
            "part-lub-001": {
                "id": "part-lub-001",
                "name": "High-Temp Synthetic Lubricant",
                "keywords": ["lubricant", "oil", "grease", "overheating", "temperature", "friction"],
                "quantity": 200, # In Liters
                "location": "Chemical Storage, Bay 2",
                "applicable_machine_types": ["Motor", "Pump", "Gearbox", "Compressor"]
            }
        }

        self.human_resources = {
            "tech-001": {
                "id": "tech-001",
                "name": "Alice Johnson",
                "role": "Maintenance Technician",
                "skills": ["Pump", "Motor", "Compressor"],
                "availability": "available",
                "current_assignment": None
            },
            "tech-002": {
                "id": "tech-002",
                "name": "Bob Smith",
                "role": "Maintenance Technician",
                "skills": ["Robotics", "HVAC"],
                "availability": "busy",
                "current_assignment": "ROBOT-J-15"
            },
            "tech-003": {
                "id": "tech-003",
                "name": "Carol Davis",
                "role": "Senior Maintenance Engineer",
                "skills": ["Turbine", "Gearbox", "Motor"],
                "availability": "available",
                "current_assignment": None
            },
            "op-001": {
                "id": "op-001",
                "name": "Dave Wilson",
                "role": "Machine Operator",
                "skills": ["Pump", "Motor"],
                "availability": "busy",
                "current_assignment": "PUMP-A-01"
            },
            "op-002": {
                "id": "op-002",
                "name": "Eve Brown",
                "role": "Machine Operator",
                "skills": ["Gearbox", "Compressor"],
                "availability": "busy",
                "current_assignment": "GEARBOX-F-03"
            }
        }

    def get_machine_details(self, machine_id: str) -> Dict[str, Any]:
        """Get detailed data for a specific machine."""
        if machine_id in self.machine_details:
            return self.machine_details[machine_id]
        return {"error": f"Machine {machine_id} not found"}

    def get_inventory(self) -> List[Dict[str, Any]]:
        """Returns the entire inventory list."""
        return list(self.inventory.values())

    def get_technicians(self) -> List[Dict[str, Any]]:
        """Returns the entire list of technicians."""
        return list(self.human_resources.values())

    def get_machine_info(self, machine_id: str) -> Dict[str, Any]:
        """Gets basic info for a machine, like its type."""
        return self.machines.get(machine_id, {"error": "Machine not found"})