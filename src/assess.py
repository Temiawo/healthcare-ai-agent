def assess_record(record: dict, summary: dict) -> dict:
    """
    Assess function: evaluates patient data for risks,
    flags dangerous values, and assigns a risk score.
    """

    flags = []
    risk_score = 0

    # --- Vitals Assessment ---
    bp = record["vitals"]["blood_pressure"]
    systolic = int(bp.split("/")[0])
    diastolic = int(bp.split("/")[1])

    if systolic >= 140 or diastolic >= 90:
        flags.append({
            "type": "CRITICAL",
            "category": "Blood Pressure",
            "message": f"Hypertension detected: {bp} — immediate review recommended",
            "value": bp
        })
        risk_score += 30
    elif systolic >= 130 or diastolic >= 80:
        flags.append({
            "type": "WARNING",
            "category": "Blood Pressure",
            "message": f"Elevated blood pressure: {bp} — monitor closely",
            "value": bp
        })
        risk_score += 15

    heart_rate = record["vitals"]["heart_rate"]
    if heart_rate > 100:
        flags.append({
            "type": "WARNING",
            "category": "Heart Rate",
            "message": f"Elevated heart rate: {heart_rate} bpm",
            "value": heart_rate
        })
        risk_score += 10

    # --- Lab Results Assessment ---
    hba1c = record["lab_results"]["HbA1c"]
    if hba1c >= 8.0:
        flags.append({
            "type": "CRITICAL",
            "category": "HbA1c",
            "message": f"Poor diabetes control: HbA1c {hba1c}% — urgent intervention needed",
            "value": hba1c
        })
        risk_score += 30
    elif hba1c >= 7.0:
        flags.append({
            "type": "WARNING",
            "category": "HbA1c",
            "message": f"Suboptimal diabetes control: HbA1c {hba1c}%",
            "value": hba1c
        })
        risk_score += 15

    cholesterol = record["lab_results"]["cholesterol"]
    if cholesterol >= 240:
        flags.append({
            "type": "CRITICAL",
            "category": "Cholesterol",
            "message": f"High cholesterol: {cholesterol} mg/dL",
            "value": cholesterol
        })
        risk_score += 20
    elif cholesterol >= 200:
        flags.append({
            "type": "WARNING",
            "category": "Cholesterol",
            "message": f"Borderline high cholesterol: {cholesterol} mg/dL",
            "value": cholesterol
        })
        risk_score += 10

    glucose = record["lab_results"]["blood_glucose"]
    if glucose >= 200:
        flags.append({
            "type": "CRITICAL",
            "category": "Blood Glucose",
            "message": f"Critically high blood glucose: {glucose} mg/dL",
            "value": glucose
        })
        risk_score += 25
    elif glucose >= 126:
        flags.append({
            "type": "WARNING",
            "category": "Blood Glucose",
            "message": f"Elevated blood glucose: {glucose} mg/dL",
            "value": glucose
        })
        risk_score += 10

    # --- Allergy Check ---
    if record["allergies"]:
        flags.append({
            "type": "INFO",
            "category": "Allergies",
            "message": f"Known allergies on file: {', '.join(record['allergies'])}",
            "value": record["allergies"]
        })

    # --- Risk Level ---
    if risk_score >= 60:
        risk_level = "HIGH"
    elif risk_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # --- Critical flag check ---
    has_critical = any(f["type"] == "CRITICAL" for f in flags)

    assessment = {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "has_critical_flags": has_critical,
        "flags": flags,
        "total_flags": len(flags),
        "requires_immediate_attention": has_critical or risk_score >= 60,
        "assessment_summary": f"Patient has {len(flags)} flag(s) with a risk score of {risk_score}/100. Risk level: {risk_level}."
    }

    print(f"⚕️  Assessment complete — Risk Level: {risk_level} (Score: {risk_score})")
    if has_critical:
        print(f"🚨 CRITICAL FLAGS DETECTED — immediate attention required!")

    return assessment


if __name__ == "__main__":
    import sys
    import os
    import json
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.gather import load_mock_record
    from src.transform import transform_record

    record = load_mock_record()
    summary = transform_record(record)
    assessment = assess_record(record, summary)
    print(json.dumps(assessment, indent=2))