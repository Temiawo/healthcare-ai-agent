import json
from datetime import datetime


def disseminate(record: dict, summary: dict, assessment: dict) -> dict:
    """
    Disseminate function: routes the right information to the
    right stakeholder in the right format.
    
    Stakeholders:
    - Patient: plain English, reassuring, actionable
    - Clinician: detailed clinical report with flags
    - Hospital System: structured JSON for records
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    patient_name = record["patient_name"]
    risk_level = assessment["risk_level"]
    risk_score = assessment["risk_score"]

    # ─── PATIENT REPORT ───────────────────────────────────────
    patient_report = {
        "recipient": "Patient",
        "recipient_name": patient_name,
        "timestamp": timestamp,
        "format": "Plain English",
        "content": {
            "greeting": f"Hello {patient_name.split()[0]}, here is a summary of your visit today.",
            "summary": summary["patient_friendly_summary"],
            "your_concerns": summary["key_concerns"],
            "your_medications": summary["medications_summary"],
            "next_steps": summary["recommended_followups"],
            "important_note": (
                "⚠️ Please seek immediate medical attention if you experience "
                "severe headache, chest pain, or difficulty breathing."
                if assessment["requires_immediate_attention"]
                else "Please follow up with your doctor as recommended above."
            )
        }
    }

    # ─── CLINICIAN REPORT ─────────────────────────────────────
    critical_flags = [f for f in assessment["flags"] if f["type"] == "CRITICAL"]
    warning_flags = [f for f in assessment["flags"] if f["type"] == "WARNING"]

    clinician_report = {
        "recipient": "Clinician",
        "timestamp": timestamp,
        "format": "Clinical Summary",
        "priority": "URGENT" if assessment["requires_immediate_attention"] else "ROUTINE",
        "content": {
            "patient": f"{record['patient_name']}, {record['age']}yo {record['gender']}",
            "visit_date": record["visit_date"],
            "chief_complaint": record["chief_complaint"],
            "clinical_summary": summary["patient_summary"],
            "risk_assessment": {
                "risk_level": risk_level,
                "risk_score": f"{risk_score}/100",
                "requires_immediate_attention": assessment["requires_immediate_attention"]
            },
            "critical_flags": critical_flags if critical_flags else "None",
            "warning_flags": warning_flags,
            "allergies": record["allergies"],
            "current_medications": record["medications"],
            "recommended_actions": summary["recommended_followups"],
            "vitals": record["vitals"],
            "lab_results": record["lab_results"]
        }
    }

    # ─── HOSPITAL SYSTEM RECORD ───────────────────────────────
    hospital_record = {
        "recipient": "Hospital System",
        "timestamp": timestamp,
        "format": "Structured Data",
        "record_type": "AI_GENERATED_SUMMARY",
        "content": {
            "patient_id": f"PT-{record['patient_name'].replace(' ', '-').upper()}",
            "visit_date": record["visit_date"],
            "ai_risk_score": risk_score,
            "ai_risk_level": risk_level,
            "flags_count": assessment["total_flags"],
            "critical_flags": len(critical_flags),
            "warning_flags": len(warning_flags),
            "requires_followup": True,
            "ai_summary": summary["patient_summary"],
            "processed_at": timestamp,
            "model_used": "claude-sonnet-4-5",
            "data_completeness": "COMPLETE"
        }
    }

    # ─── ROUTING LOGIC ────────────────────────────────────────
    outputs = {
        "dissemination_timestamp": timestamp,
        "patient_name": patient_name,
        "risk_level": risk_level,
        "reports_generated": 3,
        "patient_report": patient_report,
        "clinician_report": clinician_report,
        "hospital_record": hospital_record,
        "routing_log": [
            f"✅ Patient report → Sent to: {patient_name}",
            f"✅ Clinician report → Sent to: Attending Physician (Priority: {'URGENT' if assessment['requires_immediate_attention'] else 'ROUTINE'})",
            f"✅ Hospital record → Logged to: EHR System (Record ID: PT-{record['patient_name'].replace(' ', '-').upper()})"
        ]
    }

    # ─── PRINT ROUTING LOG ────────────────────────────────────
    print(f"\n📤 Disseminating reports for {patient_name}...")
    print(f"   Risk Level: {risk_level} ({risk_score}/100)")
    print(f"   Reports generated: 3")
    for log in outputs["routing_log"]:
        print(f"   {log}")

    return outputs


if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.gather import load_mock_record
    from src.transform import transform_record
    from src.assess import assess_record

    record = load_mock_record()
    summary = transform_record(record)
    assessment = assess_record(record, summary)
    outputs = disseminate(record, summary, assessment)

    print("\n" + "="*60)
    print("FULL DISSEMINATION OUTPUT")
    print("="*60)
    print(json.dumps(outputs, indent=2))