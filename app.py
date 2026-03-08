import streamlit as st
import re
from pypdf import PdfReader
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

from fraud_agent import evaluate_fraud
from sales_agent import evaluate_sales
import streamlit as st
import re
from pypdf import PdfReader
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

from sales_agent import evaluate_sales
from risk_agent import evaluate_risk
from compliance_agent import evaluate_compliance
from fraud_agent import evaluate_fraud
from ai_risk_model import calculate_ai_risk_score, assign_credit_grade
from ml_pd_model import predict_probability_of_default, get_model_metrics
from db import init_db, save_decision, get_all_decisions, reset_db

st.set_page_config(page_title="LendSynthetix - AI Loan War Room", layout="wide")

init_db()


# -------------------------------------------------
# LOGIN
# -------------------------------------------------
def login_screen():
    st.title("🔐 LendSynthetix Login")
    st.write("Demo credentials: admin / admin123")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid Username or Password")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_screen()
    st.stop()


# -------------------------------------------------
# MAIN UI
# -------------------------------------------------
st.title("🏦 LendSynthetix - AI Loan Underwriting System")
st.write("Agentic AI-Based Automated Loan Decision Platform")


# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


def extract_financial_metrics(text):
    def find_value(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return float(match.group(1)) if match else 0.0

    revenue = find_value(r"Revenue:\s*(\d+(\.\d+)?)")
    ebitda = find_value(r"EBITDA:\s*(\d+(\.\d+)?)")
    debt = find_value(r"Debt:\s*(\d+(\.\d+)?)")
    equity = find_value(r"Equity:\s*(\d+(\.\d+)?)")
    interest = find_value(r"Interest:\s*(\d+(\.\d+)?)")

    debt_to_equity = (debt / equity) if equity else 0.0
    dscr = (ebitda / interest) if interest else 0.0

    return {
        "Revenue": revenue,
        "EBITDA": ebitda,
        "Debt": debt,
        "Equity": equity,
        "Interest": interest,
        "Debt_to_Equity": round(debt_to_equity, 2),
        "DSCR": round(dscr, 2)
    }


def gauge_chart(value, title, bands, bar_color="darkblue"):
    steps = [{"range": [a, b], "color": c} for a, b, c in bands]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={
            "axis": {"range": [bands[0][0], bands[-1][1]]},
            "bar": {"color": bar_color},
            "steps": steps,
        }
    ))
    st.plotly_chart(fig, use_container_width=True)


def financial_bar(metrics):
    labels = ["Revenue", "EBITDA", "Debt", "Equity"]
    values = [metrics["Revenue"], metrics["EBITDA"], metrics["Debt"], metrics["Equity"]]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(labels, values)
    ax.set_title("Financial Overview")
    ax.set_ylabel("Amount")
    st.pyplot(fig)


def ratios_bar(metrics):
    labels = ["DSCR", "Debt_to_Equity"]
    values = [metrics["DSCR"], metrics["Debt_to_Equity"]]

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.bar(labels, values)
    ax.set_title("Key Ratios")
    ax.set_ylabel("Value")
    st.pyplot(fig)


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("⚙ Admin Controls")
if st.sidebar.button("Reset Loan History Database"):
    reset_db()
    st.sidebar.success("Database cleared successfully!")


# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------
uploaded_file = st.file_uploader("📄 Upload Loan Financial PDF", type="pdf")

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    metrics = extract_financial_metrics(text)

    st.subheader("📊 Extracted Financial Metrics")
    st.json(metrics)

    # Agents
    sales_result = evaluate_sales(metrics)
    risk_result = evaluate_risk(metrics)
    compliance_result = evaluate_compliance(metrics)
    fraud_result = evaluate_fraud(metrics)

    st.subheader("🤝 Agent Decisions")
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    with c1:
        st.markdown("### Sales Agent")
        st.json(sales_result)

    with c2:
        st.markdown("### Risk Agent")
        st.json(risk_result)

    with c3:
        st.markdown("### Compliance Agent")
        st.json(compliance_result)

    with c4:
        st.markdown("### Fraud Detection Agent")
        st.json(fraud_result)

    # AI score
    ai_score = calculate_ai_risk_score(metrics)
    credit_grade = assign_credit_grade(ai_score)

    # ML PD
    pd_value = predict_probability_of_default(metrics)
    if pd_value < 20:
        risk_category = "LOW RISK"
    elif pd_value < 50:
        risk_category = "MEDIUM RISK"
    else:
        risk_category = "HIGH RISK"

    st.subheader("📈 Risk Visualizations")
    left, right = st.columns(2)

    with left:
        st.markdown("### 🧠 AI Risk Score")
        st.write(f"AI Risk Score: {ai_score}")
        st.write(f"Credit Grade: {credit_grade}")
        gauge_chart(
            float(ai_score),
            "AI Risk Score (0–100)",
            bands=[(0, 40, "red"), (40, 70, "orange"), (70, 100, "green")],
            bar_color="darkblue",
        )

    with right:
        st.markdown("### 📉 Probability of Default (ML)")
        st.write(f"PD (%): {pd_value}")
        st.write(f"Risk Category: {risk_category}")
        gauge_chart(
            float(pd_value),
            "Probability of Default (%)",
            bands=[(0, 20, "green"), (20, 50, "yellow"), (50, 100, "red")],
            bar_color="crimson",
        )

    st.subheader("🚨 Fraud Risk Analysis")
    st.write("Fraud Score:", fraud_result["Fraud_Score"])
    st.write("Fraud Status:", fraud_result["Fraud_Status"])

    if fraud_result["Fraud_Status"] == "HIGH":
        st.error("High fraud suspicion detected")
    elif fraud_result["Fraud_Status"] == "MEDIUM":
        st.warning("Moderate fraud suspicion detected")
    else:
        st.success("Low fraud suspicion")

    st.subheader("📊 Financial Charts")
    cc1, cc2 = st.columns(2)

    with cc1:
        financial_bar(metrics)

    with cc2:
        ratios_bar(metrics)

    st.subheader("🧪 Model Evaluation Dashboard (ML PD Model)")
    accuracy, cm, fpr, tpr, roc_auc = get_model_metrics()

    k1, k2 = st.columns(2)
    with k1:
        st.metric("Accuracy", f"{accuracy * 100:.2f}%")
    with k2:
        st.metric("ROC AUC", f"{roc_auc:.3f}")

    st.write("Confusion Matrix:")
    st.write(cm)

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
    ax.plot([0, 1], [0, 1], linestyle="--")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend()
    st.pyplot(fig)

    # Final decision
    if fraud_result.get("Fraud_Status") == "HIGH":
        final_decision = "REJECTED (Suspected Fake Data)"
    elif compliance_result.get("Compliance_Status") == "BLOCK":
        final_decision = "REJECTED"
    elif risk_result.get("Risk_Decision") == "REJECT":
        final_decision = "REJECTED"
    elif fraud_result.get("Fraud_Status") == "MEDIUM":
        final_decision = "MANUAL REVIEW REQUIRED"
    else:
        final_decision = "APPROVED"

    st.subheader("🏦 Final Loan Decision")

    if final_decision == "APPROVED":
        st.success("LOAN APPROVED ✅")
    elif final_decision == "MANUAL REVIEW REQUIRED":
        st.warning("MANUAL REVIEW REQUIRED ⚠️")
    else:
        st.error(final_decision)

    # Save in DB
    save_decision(metrics, ai_score, credit_grade, pd_value, risk_category, final_decision)

    # Download report
    report_text = f"""LendSynthetix - Loan Underwriting Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Extracted Financial Metrics:
{metrics}

Agent Decisions:
Sales: {sales_result}
Risk: {risk_result}
Compliance: {compliance_result}

Fraud Analysis:
Fraud Score: {fraud_result['Fraud_Score']}
Fraud Status: {fraud_result['Fraud_Status']}
Fraud Flags: {fraud_result['Flags']}

AI Risk Score: {ai_score}
Credit Grade: {credit_grade}

Probability of Default (ML): {pd_value}%
Risk Category: {risk_category}

ML Model Evaluation:
Accuracy: {accuracy * 100:.2f}%
ROC AUC: {roc_auc:.3f}
Confusion Matrix: {cm.tolist()}

FINAL DECISION: {final_decision}
"""

    st.download_button(
        label="📥 Download Loan Decision Report (TXT)",
        data=report_text,
        file_name="Loan_Decision_Report.txt",
        mime="text/plain",
    )

st.subheader("📂 Loan Decision History (Saved in Database)")
history = get_all_decisions(limit=200)

if history:
    df = pd.DataFrame(history, columns=[
        "ID", "Timestamp", "Revenue", "DSCR",
        "Debt_to_Equity", "AI_Score", "PD", "Risk_Category", "Decision"
    ])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No saved history yet. Upload a PDF to generate and save a decision.")
