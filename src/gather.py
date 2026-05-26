import json
import os
from pathlib import Path

def load_patient_record(file_path: str) -> dict:
    """
    Gather function: loads a patient record from a JSON file.
    This simulates pulling data from a medical records system.
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Record not found: {file_path}")
    
    with open(path, "r") as f:
        record = json.load(f)
    
    print(f"✅ Loaded record for: {record.get('patient_name', 'Unknown')}")
    return record


def load_mock_record() -> dict:
    """
    Returns a hardcoded mock patient record for testing.
    """
    return {
        "patient_name": "Jane Doe",
        "age": 45,
        "gender": "Female",
        "visit_date": "2026-05-25",
        "chief_complaint": "Persistent headache and fatigue for 2 weeks",
        "vitals": {
            "blood_pressure": "138/88",
            "heart_rate": 92,
            "temperature": 98.9,
            "weight_lbs": 165
        },
        "medications": [
            "Lisinopril 10mg daily",
            "Metformin 500mg twice daily"
        ],
        "allergies": ["Penicillin"],
        "lab_results": {
            "HbA1c": 7.8,
            "cholesterol": 210,
            "blood_glucose": 145
        },
        "notes": "Patient reports increased stress at work. Follow up on diabetes management."
    }


if __name__ == "__main__":
    record = load_mock_record()
    print(json.dumps(record, indent=2))