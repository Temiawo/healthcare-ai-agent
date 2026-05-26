import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gather import load_mock_record, load_patient_record
from src.assess import assess_record


# ─── GATHER TESTS ─────────────────────────────────────────

class TestGather:

    def test_mock_record_loads(self):
        """Mock record should load successfully"""
        record = load_mock_record()
        assert record is not None

    def test_mock_record_has_required_fields(self):
        """Mock record must have all required fields"""
        record = load_mock_record()
        required_fields = [
            "patient_name", "age", "gender", "visit_date",
            "chief_complaint", "vitals", "medications",
            "allergies", "lab_results", "notes"
        ]
        for field in required_fields:
            assert field in record, f"Missing field: {field}"

    def test_mock_record_has_vitals(self):
        """Vitals must include blood pressure and heart rate"""
        record = load_mock_record()
        assert "blood_pressure" in record["vitals"]
        assert "heart_rate" in record["vitals"]
        assert "temperature" in record["vitals"]

    def test_mock_record_has_lab_results(self):
        """Lab results must include HbA1c, cholesterol, glucose"""
        record = load_mock_record()
        assert "HbA1c" in record["lab_results"]
        assert "cholesterol" in record["lab_results"]
        assert "blood_glucose" in record["lab_results"]

    def test_mock_record_patient_name(self):
        """Patient name should be a non-empty string"""
        record = load_mock_record()
        assert isinstance(record["patient_name"], str)
        assert len(record["patient_name"]) > 0

    def test_file_not_found_raises_error(self):
        """Loading a non-existent file should raise FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            load_patient_record("data/nonexistent.json")


# ─── ASSESS TESTS ─────────────────────────────────────────

class TestAssess:

    def get_base_record(self):
        """Returns a clean base record for testing"""
        return {
            "patient_name": "Test Patient",
            "age": 40,
            "gender": "Male",
            "visit_date": "2026-05-26",
            "chief_complaint": "Routine checkup",
            "vitals": {
                "blood_pressure": "120/80",
                "heart_rate": 75,
                "temperature": 98.6,
                "weight_lbs": 170
            },
            "medications": ["Aspirin 81mg daily"],
            "allergies": [],
            "lab_results": {
                "HbA1c": 5.5,
                "cholesterol": 180,
                "blood_glucose": 95
            },
            "notes": "Healthy patient."
        }

    def get_base_summary(self):
        """Returns a mock summary for testing"""
        return {
            "patient_summary": "Healthy patient.",
            "key_concerns": [],
            "medications_summary": "Aspirin 81mg daily.",
            "recommended_followups": ["Annual checkup"],
            "patient_friendly_summary": "You are in good health."
        }

    def test_healthy_patient_low_risk(self):
        """A healthy patient should score LOW risk"""
        record = self.get_base_record()
        summary = self.get_base_summary()
        assessment = assess_record(record, summary)
        assert assessment["risk_level"] == "LOW"
        assert assessment["risk_score"] < 30

    def test_assessment_has_required_fields(self):
        """Assessment must return all required fields"""
        record = self.get_base_record()
        summary = self.get_base_summary()
        assessment = assess_record(record, summary)
        required = [
            "risk_score", "risk_level", "has_critical_flags",
            "flags", "total_flags", "requires_immediate_attention",
            "assessment_summary"
        ]
        for field in required:
            assert field in assessment, f"Missing field: {field}"

    def test_high_blood_pressure_flagged(self):
        """Systolic BP >= 140 should trigger a CRITICAL flag"""
        record = self.get_base_record()
        record["vitals"]["blood_pressure"] = "145/92"
        summary = self.get_base_summary()
        assessment = assess_record(record, summary)
        flag_categories = [f["category"] for f in assessment["flags"]]
        assert "Blood Pressure" in flag_categories

    def test_elevated_bp_warning(self):
        """Systolic BP >= 130 should trigger a WARNING"""
        record = self.get_base_record()
        record["vitals"]["blood_pressure"] = "132/84"
        summary = self.get_base_summary()
        assessment = assess_record(record, summary)
        bp_flags = [f for f in assessment["flags"]
                    if f["category"] == "Blood Pressure"]
        assert len(bp_flags) > 0
        assert bp_flags[0]["type"] == "WARNING"

    def test_critical_hba1c_flagged(self):
        """HbA1c >= 8.0 should trigger a CRITICAL flag"""
        record = self.get_base_record()
        record["lab_results"]["HbA1c"] = 8.5
        summary = self.get_base_summary()
        assessment = assess_record(record, summary)
        assert assessment["has_critical_flags"] is True

    def test_high_risk_score_triggers_attention(self):
        """Risk score >= 60 should require immediate attention"""
        record = self.get_base_record()
        record["vitals"]["blood_pressure"] = "145/95"
        record["lab_results"]["HbA1c"] = 8.5
        record["lab_results"]["cholesterol"] = 245
        summary = self.get_base_summary()
        assessment = assess_record(record, summary)
        assert assessment["risk_score"] >= 60
        assert assessment["requires_immediate_attention"] is True

    def test_allergy_always_flagged(self):
        """Known allergies should always appear as INFO flag"""
        record = self.get_base_record()
        record["allergies"] = ["Penicillin"]
        summary = self.get_base_summary()
        assessment = assess_record(record, summary)
        allergy_flags = [f for f in assessment["flags"]
                         if f["category"] == "Allergies"]
        assert len(allergy_flags) > 0

    def test_risk_score_is_numeric(self):
        """Risk score must be a number between 0 and 100"""
        record = self.get_base_record()
        summary = self.get_base_summary()
        assessment = assess_record(record, summary)
        assert isinstance(assessment["risk_score"], (int, float))
        assert 0 <= assessment["risk_score"] <= 100

    def test_jane_doe_medium_risk(self):
        """Jane Doe's record should score MEDIUM risk"""
        record = load_mock_record()
        summary = self.get_base_summary()
        assessment = assess_record(record, summary)
        assert assessment["risk_level"] == "MEDIUM"
        assert assessment["risk_score"] == 50