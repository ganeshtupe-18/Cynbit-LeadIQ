# Cynbit LeadIQ — AI-Powered Lead Intelligence

A functional proof of concept for qualifying inbound project inquiries for a digital engineering and AI services company.

## Why this opportunity?
Cynbit publicly describes AI automation, autonomous agents, CRM automation, custom software, cloud infrastructure and an inquiry hub that prepares tailored project overviews. LeadIQ is a proposed extension: turn an unstructured inquiry into a structured, prioritized lead brief for human review.

This is a proposal, not a claim that Cynbit currently has this workflow or has provided customer data.

## Features
- Predicts one of five service categories using TF-IDF + Logistic Regression.
- Estimates sentiment using VADER.
- Calculates an explainable 0–100 lead score with transparent rules.
- Assigns High / Medium / Low priority.
- Identifies basic missing qualification details.
- Drafts an editable first response.
- Includes three sample inquiries.

## Run locally
```bash
# Python 3.10+
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```
Open the local URL printed by Streamlit (normally http://localhost:8501).

## Project structure
```text
Cynbit_LeadIQ/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── synthetic_inquiries.csv
└── reports/
    ├── AI_Opportunity_Report.md
    └── Technical_Approach_Report.md
```

## Model and data notes
The classifier is trained at app startup on a small, hand-written synthetic dataset embedded in `app.py`. The CSV in `data/` is a separate inspectable copy of example training rows. These examples are not real Cynbit leads. The model is a demonstration of the pipeline, not a production-ready classifier. Confidence scores should not be interpreted as calibrated probabilities.

## Limitations and responsible use
- No real customer data, CRM connection, email sending, or external LLM/API is used.
- Synthetic training examples are small and may not generalize to real inquiries.
- Sentiment can be wrong for sarcasm, mixed language, or domain-specific language.
- Rule-based lead scoring is illustrative and must be calibrated with business stakeholders.
- Do not use the score to automatically reject a prospect.
- Production deployment requires consent, access controls, encryption, retention rules, audit logs, evaluation on representative anonymized data, and human approval.

## Suggested GitHub publishing steps
```bash
git init
git add .
git commit -m "Build Cynbit LeadIQ AI lead qualification POC"
git branch -M main
git remote add origin https://github.com/<your-username>/cynbit-leadiq.git
git push -u origin main
```

## Suggested live deployment
1. Push the repository to GitHub.
2. Open https://share.streamlit.io/
3. Connect GitHub and select this repository.
4. Choose `app.py` as the main file.
5. Deploy and test the public URL in an incognito browser.

## Assessment deliverables
- `reports/AI_Opportunity_Report.md`
- `reports/Technical_Approach_Report.md`
- This running Streamlit POC.
