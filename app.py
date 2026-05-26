import streamlit as st
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.gather import load_mock_record, load_patient_record
from src.transform import transform_record
from src.assess import assess_record
from src.disseminate import disseminate

# ─── PAGE CONFIG ──────────────────────────────────────────
st.set_page_config(
    page_title="Healthcare AI Agent",
    page_icon="🏥",
    layout="wide"
)

# ─── HEADER ───────────────────────────────────────────────
st.title("🏥 Healthcare AI Agent")
st.markdown("**AI-powered patient record analysis — Purdue University MS Research Project**")
st.markdown("*Powered by Claude (Anthropic) | Researching direct & social alignment in healthcare AI*")
st.divider()

# ─── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Controls")
    use_mock = st.toggle("Use mock patient record", value=True)

    if not use_mock:
        uploaded_file = st.file_uploader(
            "Upload patient record (JSON)",
            type=["json"]
        )

    st.divider()
    st.markdown("### About this project")
    st.markdown("""
    This AI agent demonstrates four core functions:
    - 📥 **Gather** — load patient data
    - 🔄 **Transform** — AI summarization
    - ⚕️ **Assess** — risk scoring
    - 📤 **Disseminate** — stakeholder routing
    """)
    st.markdown("**Research focus:** Principal-agent alignment across patients, clinicians, and hospitals")

# ─── MAIN CONTENT ─────────────────────────────────────────
if st.button("🚀 Run AI Agent", type="primary", use_container_width=True):

    # Step 1 - Gather
    with st.status("Running AI Agent...", expanded=True) as status:

        st.write("📥 Step 1: Gathering patient record...")
        try:
            if use_mock:
                record = load_mock_record()
            else:
                if uploaded_file:
                    record = json.load(uploaded_file)
                else:
                    st.error("Please upload a patient record file")
                    st.stop()
            st.write(f"✅ Record loaded for: **{record['patient_name']}**")

            # Step 2 - Transform
            st.write("🤖 Step 2: Transforming with Claude AI...")
            summary = transform_record(record)
            st.write("✅ AI transformation complete!")

            # Step 3 - Assess
            st.write("⚕️ Step 3: Assessing risk...")
            assessment = assess_record(record, summary)
            st.write(f"✅ Risk assessment complete — Level: **{assessment['risk_level']}**")

            # Step 4 - Disseminate
            st.write("📤 Step 4: Disseminating reports...")
            outputs = disseminate(record, summary, assessment)
            st.write("✅ All reports generated and routed!")

            status.update(label="✅ Agent completed successfully!", state="complete")

        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"Error: {str(e)}")
            st.stop()

    st.divider()

    # ─── RISK OVERVIEW ────────────────────────────────────
    st.subheader("📊 Risk Overview")
    col1, col2, col3, col4 = st.columns(4)

    risk_color = {
        "LOW": "🟢",
        "MEDIUM": "🟡",
        "HIGH": "🔴"
    }

    with col1:
        st.metric("Risk Level",
                  f"{risk_color[assessment['risk_level']]} {assessment['risk_level']}")
    with col2:
        st.metric("Risk Score", f"{assessment['risk_score']}/100")
    with col3:
        st.metric("Total Flags", assessment['total_flags'])
    with col4:
        st.metric("Immediate Attention",
                  "⚠️ YES" if assessment['requires_immediate_attention'] else "✅ NO")

    # ─── FLAGS ────────────────────────────────────────────
    if assessment["flags"]:
        st.subheader("🚩 Clinical Flags")
        for flag in assessment["flags"]:
            if flag["type"] == "CRITICAL":
                st.error(f"🚨 **CRITICAL — {flag['category']}:** {flag['message']}")
            elif flag["type"] == "WARNING":
                st.warning(f"⚠️ **WARNING — {flag['category']}:** {flag['message']}")
            else:
                st.info(f"ℹ️ **INFO — {flag['category']}:** {flag['message']}")

    st.divider()

    # ─── THREE STAKEHOLDER REPORTS ────────────────────────
    st.subheader("📋 Stakeholder Reports")
    tab1, tab2, tab3 = st.tabs(["👤 Patient Report", "👨‍⚕️ Clinician Report", "🏥 Hospital Record"])

    # Patient tab
    with tab1:
        patient = outputs["patient_report"]["content"]
        st.markdown(f"### {patient['greeting']}")
        st.markdown(f"**Summary:** {patient['summary']}")
        st.markdown("**Your health concerns:**")
        for concern in patient["your_concerns"]:
            st.markdown(f"- {concern}")
        st.markdown(f"**Your medications:** {patient['your_medications']}")
        st.markdown("**Your next steps:**")
        for step in patient["next_steps"]:
            st.markdown(f"- ✅ {step}")
        st.info(patient["important_note"])

    # Clinician tab
    with tab2:
        clinician = outputs["clinician_report"]["content"]
        priority = outputs["clinician_report"]["priority"]
        if priority == "URGENT":
            st.error(f"🚨 Priority: {priority}")
        else:
            st.success(f"✅ Priority: {priority}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Patient:** {clinician['patient']}")
            st.markdown(f"**Visit Date:** {clinician['visit_date']}")
            st.markdown(f"**Chief Complaint:** {clinician['chief_complaint']}")
            st.markdown(f"**Allergies:** {', '.join(clinician['allergies'])}")
        with col2:
            st.markdown("**Vitals:**")
            for k, v in clinician["vitals"].items():
                st.markdown(f"- {k.replace('_', ' ').title()}: {v}")

        st.markdown(f"**Clinical Summary:** {clinician['clinical_summary']}")
        st.markdown("**Recommended Actions:**")
        for action in clinician["recommended_actions"]:
            st.markdown(f"- {action}")

    # Hospital tab
    with tab3:
        hospital = outputs["hospital_record"]["content"]
        st.json(hospital)

    st.divider()

    # ─── RAW OUTPUT ───────────────────────────────────────
    with st.expander("🔍 View full raw agent output (JSON)"):
        st.json(outputs)