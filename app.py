import streamlit as st
import pandas as pd
import re
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="Cynbit LeadIQ", page_icon="🎯", layout="wide")

# Small, transparent synthetic training set for a reproducible demonstration.
TRAINING = [
    ("Need a modern ecommerce website with payment gateway and product catalogue", "Web Development"),
    ("Our company website is outdated and needs a complete redesign", "Web Development"),
    ("Build a mobile application for Android and iOS with user login", "Web Development"),
    ("We need a customer portal and admin dashboard", "Web Development"),
    ("Create a React frontend and backend API for our startup", "Web Development"),
    ("Need an online booking website with database integration", "Web Development"),
    ("Develop a SaaS platform for managing subscriptions", "Web Development"),
    ("We want to migrate our old web application to a modern stack", "Web Development"),
    ("Can you build a responsive website for our business", "Web Development"),
    ("Need a landing page and web application for product launch", "Web Development"),
    ("We want an AI chatbot for customer support", "AI/ML & Automation"),
    ("Automate invoice processing using OCR and artificial intelligence", "AI/ML & Automation"),
    ("Build an LLM agent to answer questions from company documents", "AI/ML & Automation"),
    ("We need machine learning for predicting customer churn", "AI/ML & Automation"),
    ("Develop an AI voice agent to handle incoming calls", "AI/ML & Automation"),
    ("Integrate a RAG assistant into our existing SaaS product", "AI/ML & Automation"),
    ("Automate repetitive business workflows with AI agents", "AI/ML & Automation"),
    ("We need sentiment analysis for customer reviews", "AI/ML & Automation"),
    ("Build a recommendation engine for our ecommerce platform", "AI/ML & Automation"),
    ("Can you create an intelligent document extraction system", "AI/ML & Automation"),
    ("We need AWS infrastructure and cloud deployment", "Cloud & DevOps"),
    ("Set up CI CD pipelines using Docker and Kubernetes", "Cloud & DevOps"),
    ("Our application needs scalable cloud architecture", "Cloud & DevOps"),
    ("Migrate our servers and database to Azure", "Cloud & DevOps"),
    ("We need monitoring backups and secure cloud hosting", "Cloud & DevOps"),
    ("Improve deployment automation and infrastructure reliability", "Cloud & DevOps"),
    ("Configure AWS networking and production environments", "Cloud & DevOps"),
    ("Help us containerize our application with Docker", "Cloud & DevOps"),
    ("We need cloud cost optimization and performance monitoring", "Cloud & DevOps"),
    ("Design a secure scalable infrastructure for our platform", "Cloud & DevOps"),
    ("We need CRM setup and automated lead follow up", "CRM & Marketing"),
    ("Automate email campaigns and customer segmentation", "CRM & Marketing"),
    ("Improve our website SEO and organic search traffic", "CRM & Marketing"),
    ("We need a sales funnel and lead nurturing automation", "CRM & Marketing"),
    ("Manage Google ads and track marketing conversions", "CRM & Marketing"),
    ("Connect our CRM with website forms and email notifications", "CRM & Marketing"),
    ("Build a marketing analytics dashboard for campaign ROI", "CRM & Marketing"),
    ("We need social media marketing and content planning", "CRM & Marketing"),
    ("Help us generate qualified leads for our services", "CRM & Marketing"),
    ("Optimize landing pages to increase conversion rates", "CRM & Marketing"),
    ("We need a technical consultation for our software architecture", "Consulting"),
    ("Please arrange a discovery call to discuss our product idea", "Consulting"),
    ("We are exploring technology options for a new business", "Consulting"),
    ("Need an estimate and project roadmap before development", "Consulting"),
    ("Can your team review our existing system architecture", "Consulting"),
    ("We need advice on choosing the right technology stack", "Consulting"),
    ("Please share your process timeline and engagement model", "Consulting"),
    ("We want a technical feasibility assessment for our idea", "Consulting"),
    ("Can we schedule a meeting with your engineering team", "Consulting"),
    ("Need a proposal for a digital transformation project", "Consulting"),
]

@st.cache_resource
def train_classifier():
    x = [x[0] for x in TRAINING]
    y = [x[1] for x in TRAINING]
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), stop_words="english", min_df=1)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])
    model.fit(x, y)
    return model

model = train_classifier()
sentiment_analyzer = SentimentIntensityAnalyzer()

def priority_and_score(text, sentiment):
    t = text.lower()
    urgency_terms = ["urgent", "asap", "immediately", "today", "tomorrow", "deadline", "critical", "within 24 hours"]
    budget_terms = ["budget", "₹", "inr", "usd", "$", " lakh", " lac", "million"]
    timeline_terms = ["this week", "next week", "this month", "launch", "deadline", "within"]
    detail_terms = ["users", "features", "integration", "database", "api", "dashboard", "payment", "mobile", "cloud"]
    score = 25
    score += 25 if any(k in t for k in urgency_terms) else 0
    score += 15 if any(k in t for k in budget_terms) else 0
    score += 15 if any(k in t for k in timeline_terms) else 0
    score += 15 if any(k in t for k in detail_terms) else 0
    score += 5 if len(text.split()) >= 25 else 0
    score = min(score, 100)
    if any(k in t for k in urgency_terms) or sentiment == "Negative":
        priority = "High"
    elif score >= 60:
        priority = "Medium"
    else:
        priority = "Low"
    return priority, score

def draft_reply(category, priority):
    timing = {
        "High": "We will prioritize an initial review and aim to coordinate a discovery discussion promptly.",
        "Medium": "Our team can review the requirements and coordinate a suitable discovery discussion.",
        "Low": "We would be happy to learn more and recommend an appropriate next step."
    }[priority]
    return (
        f"Thank you for contacting Cynbit Technologies. Based on your inquiry, "
        f"your requirement appears related to {category}. {timing} "
        "Could you please share your expected timeline, key features, approximate budget, "
        "and any existing systems or integrations? This will help us prepare a focused project brief."
    )

st.title("🎯 Cynbit LeadIQ")
st.caption("AI-powered lead qualification • Concept proof of concept • Synthetic demonstration data")

with st.sidebar:
    st.header("About this POC")
    st.write("Classifies inbound project inquiries, estimates lead priority, and drafts a suggested response.")
    st.info("This demo uses synthetic examples only. It is not connected to Cynbit's CRM or customer data.")
    st.markdown("**Model:** TF-IDF + Logistic Regression")
    st.markdown("**Scoring:** Transparent rules")

samples = {
    "AI chatbot for support": "We are a Jaipur-based retail business and urgently need an AI chatbot for customer support. It should answer product questions from our FAQ documents, integrate with our website, and support around 5,000 users. We hope to launch next month. Please share an estimate.",
    "Cloud migration": "Our startup needs to migrate its existing application and PostgreSQL database to AWS. We need Docker deployment, CI/CD, backups, monitoring, and a secure production setup within six weeks. Please arrange a technical discussion.",
    "Website redesign": "We need a responsive ecommerce website with product catalogue, payment gateway, customer login, admin dashboard, and inventory integration. We are exploring vendors and would like a project roadmap."
}

left, right = st.columns([1.15, 0.85])
with left:
    st.subheader("1. Enter a project inquiry")
    selected = st.selectbox("Load a sample inquiry", ["Custom inquiry"] + list(samples.keys()))
    default_text = samples.get(selected, "")
    inquiry = st.text_area("Customer message", value=default_text, height=220,
                           placeholder="Paste a customer project inquiry here...")
    analyze = st.button("Analyze inquiry", type="primary", use_container_width=True)

with right:
    st.subheader("2. What the system evaluates")
    st.markdown("- Service category prediction\n- Category confidence\n- Customer sentiment\n- Lead priority and score\n- Missing qualification details\n- Suggested first response")
    st.caption("Predictions are decision-support signals, not an automated business decision.")

if analyze:
    if len(inquiry.strip()) < 15:
        st.warning("Please enter a little more detail (at least 15 characters).")
    else:
        probs = model.predict_proba([inquiry])[0]
        classes = model.classes_
        idx = probs.argmax()
        category = classes[idx]
        confidence = float(probs[idx])
        compound = sentiment_analyzer.polarity_scores(inquiry)["compound"]
        sentiment = "Positive" if compound >= 0.05 else ("Negative" if compound <= -0.05 else "Neutral")
        priority, score = priority_and_score(inquiry, sentiment)

        st.divider()
        st.subheader("3. Lead intelligence results")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Predicted service", category)
        m2.metric("Model confidence", f"{confidence:.0%}")
        m3.metric("Lead score", f"{score}/100")
        m4.metric("Priority", priority)
        st.write(f"**Customer sentiment:** {sentiment}")
        st.progress(score / 100)
        if confidence < 0.60:
            st.warning(
                "Low model confidence. "
                "Please review this service category manually."
            )

        with st.expander("Category confidence breakdown"):
            st.dataframe(pd.DataFrame({"Service": classes, "Probability": probs}).sort_values("Probability", ascending=False),
                         use_container_width=True, hide_index=True)

        text_lower = inquiry.lower()
        missing = []
        if not any(k in text_lower for k in ["budget", "₹", "inr", "usd", "$", " lakh", " lac"]):
            missing.append("Approximate budget")
        if not any(k in text_lower for k in ["week", "month", "date", "deadline", "launch", "day"]):
            missing.append("Expected timeline")
        if not any(k in text_lower for k in ["users", "features", "integration", "database", "api", "dashboard"]):
            missing.append("Key features / expected scope")
        st.markdown("**Details to clarify:** " + (", ".join(missing) if missing else "No major qualification gaps detected by basic checks."))

        st.subheader("4. Suggested customer response")
        st.text_area("Editable response draft", value=draft_reply(category, priority), height=150)
        st.caption("Human review is required before sending. The POC does not send emails or update a CRM.")

st.divider()
st.caption("Cynbit LeadIQ | Internship assessment prototype | Built with Python and Streamlit")
