import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

def transform_record(record: dict) -> dict:
    """
    Transform function: sends the patient record to Claude API
    and returns a structured, human-readable summary.
    """
    
    record_text = f"""
    Patient: {record['patient_name']}, Age: {record['age']}, Gender: {record['gender']}
    Visit Date: {record['visit_date']}
    Chief Complaint: {record['chief_complaint']}
    
    Vitals:
    - Blood Pressure: {record['vitals']['blood_pressure']}
    - Heart Rate: {record['vitals']['heart_rate']} bpm
    - Temperature: {record['vitals']['temperature']}°F
    - Weight: {record['vitals']['weight_lbs']} lbs
    
    Medications: {', '.join(record['medications'])}
    Allergies: {', '.join(record['allergies'])}
    
    Lab Results:
    - HbA1c: {record['lab_results']['HbA1c']}%
    - Cholesterol: {record['lab_results']['cholesterol']} mg/dL
    - Blood Glucose: {record['lab_results']['blood_glucose']} mg/dL
    
    Clinical Notes: {record['notes']}
    """

    print("🤖 Sending record to Claude for transformation...")

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        system="""You are a clinical AI assistant helping summarize patient 
        medical records. Provide clear, structured summaries that are 
        easy to understand for both patients and clinicians. 
        Always be factual and only use information provided.""",
        messages=[
            {
                "role": "user",
                "content": f"""Please summarize this patient record and 
                return a JSON object with these exact fields:
                {{
                    "patient_summary": "2-3 sentence overview",
                    "key_concerns": ["list", "of", "main", "health", "concerns"],
                    "medications_summary": "brief medication overview",
                    "recommended_followups": ["list", "of", "follow", "up", "actions"],
                    "patient_friendly_summary": "simple plain English summary for the patient"
                }}
                
                Return ONLY the JSON object, no extra text.
                
                Patient Record:
                {record_text}"""
            }
        ]
    )

    import json
    raw = response.content[0].text.strip()
    clean = raw.replace("```json", "").replace("```", "").strip()
    summary = json.loads(clean)
    
    print("✅ Record transformed successfully!")
    return summary


if __name__ == "__main__":
    from gather import load_mock_record
    import json
    
    record = load_mock_record()
    summary = transform_record(record)
    print(json.dumps(summary, indent=2))

