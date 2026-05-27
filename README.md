# 🏥 Healthcare AI Agent
### AI-Powered Patient Record Management with Alignment Analysis

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Claude](https://img.shields.io/badge/Powered%20by-Claude%20Anthropic-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![Research](https://img.shields.io/badge/Purdue%20University-MS%20Research-gold)
![License](https://img.shields.io/badge/License-MIT-green)

 
> *Research project exploring principal-agent alignment in autonomous healthcare AI systems*

---

## 📋 Overview

This project proposes and implements an **AI Healthcare Agent** for patient-owned 
medical record management, an autonomous agentic system that delegates the 
high-volume task of medical record processing across four core functions:

| Function | Description |
|---|---|
| 📥 **Gather** | Load and retrieve patient records from medical data sources |
| 🔄 **Transform** | AI-powered summarization using Claude (Anthropic) |
| ⚕️ **Assess** | Clinical risk scoring and flag generation |
| 📤 **Disseminate** | Route context-appropriate reports to the right stakeholders |

The agent produces three distinct outputs tailored to different stakeholders:
- 👤 **Patient** — plain English summary they can actually understand
- 👨‍⚕️ **Clinician** — detailed clinical report with risk flags and recommendations  
- 🏥 **Hospital System** — structured JSON data for EHR integration


---

## 🏗️ Architecture

```
Patient Record (JSON)
        │
        ▼
┌─────────────────┐
│   GATHER        │  ← Load from file / EHR system / upload
│   gather.py     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   TRANSFORM     │  ← Claude API (Anthropic) summarization
│   transform.py  │  ← Structured JSON output
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   ASSESS        │  ← Clinical threshold checking
│   assess.py     │  ← Risk scoring (0-100)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│              DISSEMINATE                │
│            disseminate.py               │
├─────────────┬──────────────┬────────────┤
│  Patient    │  Clinician   │  Hospital  │
│  Report     │  Report      │  Record    │
│  (Plain     │  (Clinical   │  (JSON/    │
│  English)   │  Summary)    │  EHR)      │
└─────────────┴──────────────┴────────────┘
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| Claude API (Anthropic) | AI summarization & transformation |
| Streamlit | Interactive web dashboard |
| Pandas & NumPy | Data processing |
| python-dotenv | Secure API key management |
| pytest | Testing suite |
| GitHub Actions | CI/CD pipeline |

**AI Tools used in development:**
Claude API · OpenAI Codex · GitHub Copilot · Amazon Q · Kiro · Cursor AI · ChatGPT

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/healthcare-ai-agent.git
cd healthcare-ai-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your Anthropic API key to .env
```

### Configuration
Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your-api-key-here
```

### Run the Application
```bash
# Run the full Streamlit dashboard
streamlit run app.py

# Or run individual components
python src/gather.py
python src/transform.py
python src/assess.py
python src/disseminate.py
```

---

## 📁 Project Structure

```
healthcare-ai-agent/
├── data/
│   └── patient_001.json      # Mock patient records
├── src/
│   ├── gather.py             # Gather: load patient records
│   ├── transform.py          # Transform: Claude AI summarization
│   ├── assess.py             # Assess: risk scoring & flagging
│   └── disseminate.py        # Disseminate: stakeholder routing
├── tests/
│   └── test_agent.py         # Test suite
├── app.py                    # Streamlit dashboard
├── requirements.txt          # Dependencies
├── .env.example              # Environment variable template
└── README.md                 # This file
```

---

## ⚕️ How It Works

### 1. Gather
Loads patient records from JSON files simulating EHR data sources.
Extracts vitals, lab results, medications, allergies, and clinical notes.

### 2. Transform
Sends structured patient data to the **Claude API (Anthropic)** with a 
carefully crafted clinical prompt. Returns a structured JSON summary with:
- Clinical overview
- Key health concerns
- Medication summary
- Recommended follow-ups
- Patient-friendly plain English summary

### 3. Assess
Evaluates patient data against clinical thresholds:

| Metric | Warning Threshold | Critical Threshold |
|---|---|---|
| Blood Pressure (Systolic) | ≥130 | ≥140 |
| HbA1c | ≥7.0% | ≥8.0% |
| Cholesterol | ≥200 mg/dL | ≥240 mg/dL |
| Blood Glucose | ≥126 mg/dL | ≥200 mg/dL |

Generates a **risk score (0-100)** and risk level: LOW / MEDIUM / HIGH

### 4. Disseminate
Routes three distinct reports to three stakeholders:
- **Patient report** — reassuring, plain English, actionable
- **Clinician report** — full clinical detail, priority flag, recommended actions
- **Hospital record** — structured JSON for EHR integration

---

## 🔬 Alignment Analysis

> This section is the core research contribution of this project.  
> It evaluates the AI agent against direct and social alignment frameworks.

### What is Alignment?

**Direct alignment** asks: *Does the agent do what the principal intends?*  
**Social alignment** asks: *Is the agent beneficial beyond the immediate principal?*

In healthcare, these questions are especially complex because there are 
**multiple competing principals** — patients, clinicians, and hospitals — 
each with distinct goals, authority levels, and trust relationships.

---

### ⚠️ Direct Alignment Risks

| Risk | Description | Mitigation |
|---|---|---|
| **Over-summarization** | AI may omit clinically critical details when simplifying | Human-in-the-loop review for all clinical outputs |
| **Threshold drift** | Risk scoring thresholds may not match individual patient baselines | Configurable thresholds per patient profile |
| **False confidence** | Structured output may appear more certain than the underlying data warrants | Explicit uncertainty flags in all outputs |
| **Stakeholder confusion** | Agent may route information to the wrong stakeholder | Strict routing logic with access controls |
| **Principal conflict** | Patient goals may conflict with clinician recommendations | Clear principal hierarchy with patient autonomy preserved |

---

### 🌍 Social Alignment Risks

| Risk | Description | Mitigation |
|---|---|---|
| **Health data bias** | AI trained on biased datasets may produce inequitable assessments | Bias auditing on model outputs across demographics |
| **Analyst deskilling** | Over-reliance on AI may erode clinical judgment over time | AI positioned as decision support, not decision maker |
| **Information asymmetry** | Organizations with AI access gain advantage over those without | Advocate for equitable AI access across healthcare systems |
| **Patient autonomy erosion** | Patients may defer to AI recommendations without understanding them | Patient-friendly explanations always required |
| **Data privacy risk** | Centralized AI processing of medical records creates breach risk | Local processing; no data sent to third parties without consent |
| **Regulatory non-compliance** | AI outputs may conflict with HIPAA or clinical standards | Output clearly labeled AI-generated; human sign-off required |

---

### 🏛️ Governance Framework

Based on the alignment analysis, responsible deployment requires:

1. **Human-in-the-loop** — No clinical decision is made autonomously  
   without physician review
2. **Transparency** — All outputs clearly labeled as AI-generated
3. **Patient consent** — Explicit opt-in before AI processes any record
4. **Auditability** — Every agent action logged with timestamp and model version
5. **Override capability** — Clinicians can override any AI recommendation
6. **Regular recalibration** — Risk thresholds reviewed quarterly

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🔮 Future Work

- [ ] Connect to real EHR APIs (Epic, Cerner, FHIR)
- [ ] Add multi-patient batch processing
- [ ] Implement bias detection across demographic groups
- [ ] Add explainability layer (why did the agent flag this?)
- [ ] Deploy to cloud (AWS/GCP) with proper HIPAA controls
- [ ] Add multi-language patient report generation
- [ ] Implement federated learning for privacy-preserving model improvement

---


## 📄 License

MIT License — see [LICENSE](LICENSE) for details.


*This project was built as part of graduate research exploring  
the intersection of agentic AI, healthcare informatics, and AI safety alignment.*